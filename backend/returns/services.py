import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.db.models import Sum

from accounts.models import Device
from audit.models import AuditEvent
from fulfillment.models import Invoice, InvoiceItem
from payments.models import CommissionMovement

from .models import ReturnConfirmation, ReturnItem, ReturnReport


class ReturnConflictError(Exception):
    pass


@dataclass(frozen=True)
class OperationResult:
    instance: object
    created: bool


def hash_payload(payload):
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def report_return(
    *, actor, report_id, invoice_id, device_id, client_reported_at,
    items, idempotency_key, correlation_id,
):
    normalized_items = sorted(
        ({"invoice_item_id": str(item["invoice_item_id"]), "quantity": item["quantity"]} for item in items),
        key=lambda item: item["invoice_item_id"],
    )
    request_hash = hash_payload({
        "report_id": str(report_id),
        "invoice_id": str(invoice_id),
        "device_id": str(device_id),
        "client_reported_at": client_reported_at.isoformat(),
        "items": normalized_items,
    })
    existing = ReturnReport.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.seller_id != actor.pk or existing.request_hash != request_hash:
            raise ReturnConflictError
        AuditEvent.objects.create(
            actor=actor, action="return.report_idempotent_replay", resource_type="return_report",
            resource_id=str(existing.id), result=AuditEvent.Result.SUCCESS, source="android",
            correlation_id=correlation_id,
        )
        return OperationResult(existing, False)

    invoice = Invoice.objects.select_for_update().filter(
        pk=invoice_id, seller=actor, status=Invoice.Status.PAID
    ).first()
    device = Device.objects.filter(pk=device_id, user=actor, is_active=True).first()
    if not invoice or not device:
        raise ReturnConflictError
    item_ids = [item["invoice_item_id"] for item in items]
    invoice_items = InvoiceItem.objects.filter(pk__in=item_ids, invoice=invoice).in_bulk()
    if len(invoice_items) != len(item_ids):
        raise ReturnConflictError

    total = Decimal("0.00")
    commission_total = Decimal("0.00")
    return_items = []
    for item in items:
        invoice_item = invoice_items[item["invoice_item_id"]]
        returned = ReturnItem.objects.filter(invoice_item=invoice_item).aggregate(total=Sum("quantity"))["total"] or 0
        if returned + item["quantity"] > invoice_item.quantity:
            raise ReturnConflictError
        line_total = invoice_item.unit_price * item["quantity"]
        line_commission = invoice_item.unit_commission * item["quantity"]
        total += line_total
        commission_total += line_commission
        return_items.append(ReturnItem(
            invoice_item=invoice_item, quantity=item["quantity"], unit_price=invoice_item.unit_price,
            unit_commission=invoice_item.unit_commission, line_total=line_total,
            commission_total=line_commission,
        ))

    try:
        with transaction.atomic():
            report = ReturnReport.objects.create(
                id=report_id, invoice=invoice, seller=actor, device=device, total=total,
                commission_total=commission_total, idempotency_key=idempotency_key,
                request_hash=request_hash, client_reported_at=client_reported_at,
            )
            for item in return_items:
                item.return_report = report
            ReturnItem.objects.bulk_create(return_items)
    except IntegrityError as error:
        raise ReturnConflictError from error
    AuditEvent.objects.create(
        actor=actor, action="return.reported", resource_type="return_report", resource_id=str(report.id),
        result=AuditEvent.Result.SUCCESS, source="android", correlation_id=correlation_id,
        metadata={"invoice_id": str(invoice.id), "item_count": len(return_items)},
    )
    return OperationResult(report, True)


@transaction.atomic
def confirm_return(
    *, actor, confirmation_id, return_report_id, confirmed_at, idempotency_key, correlation_id,
):
    request_hash = hash_payload({
        "confirmation_id": str(confirmation_id),
        "return_report_id": str(return_report_id),
        "confirmed_at": confirmed_at.isoformat(),
    })
    existing = ReturnConfirmation.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.request_hash != request_hash:
            raise ReturnConflictError
        AuditEvent.objects.create(
            actor=actor, action="return.confirmation_idempotent_replay",
            resource_type="return_confirmation", resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS, source="web", correlation_id=correlation_id,
        )
        return OperationResult(existing, False)
    report = ReturnReport.objects.select_for_update().prefetch_related("items").filter(pk=return_report_id).first()
    if not report or report.status != ReturnReport.Status.REPORTED:
        raise ReturnConflictError
    payment_confirmation = report.invoice.payment_report.confirmation
    try:
        with transaction.atomic():
            confirmation = ReturnConfirmation.objects.create(
                id=confirmation_id, return_report=report, confirmed_by=actor, confirmed_at=confirmed_at,
                idempotency_key=idempotency_key, request_hash=request_hash,
            )
            CommissionMovement.objects.bulk_create([
                CommissionMovement(
                    seller=report.seller, invoice=report.invoice, invoice_item=item.invoice_item,
                    payment_confirmation=payment_confirmation,
                    movement_type=CommissionMovement.MovementType.DEBIT,
                    amount=item.commission_total, reference_type="return_confirmation",
                    reference_id=confirmation.id,
                ) for item in report.items.all()
            ])
    except IntegrityError as error:
        raise ReturnConflictError from error
    report.status = ReturnReport.Status.CONFIRMED
    report.version += 1
    report.save(update_fields=["status", "version", "updated_at"])
    AuditEvent.objects.create(
        actor=actor, action="return.confirmed", resource_type="return_confirmation",
        resource_id=str(confirmation.id), result=AuditEvent.Result.SUCCESS, source="web",
        correlation_id=correlation_id, metadata={"return_report_id": str(report.id)},
    )
    AuditEvent.objects.create(
        actor=actor, action="commission.debited", resource_type="return_report", resource_id=str(report.id),
        result=AuditEvent.Result.SUCCESS, source="web", correlation_id=correlation_id,
        metadata={"movement_count": report.items.count()},
    )
    return OperationResult(confirmation, True)
