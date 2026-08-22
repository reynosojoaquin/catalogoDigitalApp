import hashlib
import json
from dataclasses import dataclass

from django.db import IntegrityError, transaction

from accounts.models import Device
from audit.models import AuditEvent
from fulfillment.models import Invoice

from .models import CommissionMovement, PaymentConfirmation, PaymentReport


class PaymentIdempotencyConflictError(Exception):
    pass


class InvoiceNotPayableError(Exception):
    pass


class PaymentNotConfirmableError(Exception):
    pass


@dataclass(frozen=True)
class OperationResult:
    instance: object
    created: bool


def hash_payload(payload):
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def report_payment(
    *, actor, report_id, invoice_id, device_id, method, terminal_reference,
    client_reported_at, idempotency_key, correlation_id,
):
    request_hash = hash_payload({
        "report_id": str(report_id),
        "invoice_id": str(invoice_id),
        "device_id": str(device_id),
        "method": method,
        "terminal_reference": terminal_reference,
        "client_reported_at": client_reported_at.isoformat(),
    })
    existing = PaymentReport.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.seller_id != actor.pk or existing.request_hash != request_hash:
            raise PaymentIdempotencyConflictError
        AuditEvent.objects.create(
            actor=actor,
            action="payment.report_idempotent_replay",
            resource_type="payment_report",
            resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS,
            source="android",
            correlation_id=correlation_id,
        )
        return OperationResult(instance=existing, created=False)

    invoice = Invoice.objects.select_for_update().filter(
        pk=invoice_id,
        seller=actor,
        status=Invoice.Status.UNPAID,
    ).first()
    device = Device.objects.filter(pk=device_id, user=actor, is_active=True).first()
    if not invoice or not device or PaymentReport.objects.filter(invoice_id=invoice_id).exists():
        raise InvoiceNotPayableError

    try:
        with transaction.atomic():
            report = PaymentReport.objects.create(
                id=report_id,
                invoice=invoice,
                seller=actor,
                device=device,
                method=method,
                external_terminal_reference=terminal_reference,
                amount=invoice.total,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                client_reported_at=client_reported_at,
            )
    except IntegrityError as error:
        existing = PaymentReport.objects.filter(idempotency_key=idempotency_key).first()
        if existing and existing.seller_id == actor.pk and existing.request_hash == request_hash:
            return OperationResult(instance=existing, created=False)
        raise PaymentIdempotencyConflictError from error

    AuditEvent.objects.create(
        actor=actor,
        action="payment.reported",
        resource_type="payment_report",
        resource_id=str(report.id),
        result=AuditEvent.Result.SUCCESS,
        source="android",
        correlation_id=correlation_id,
        metadata={"invoice_id": str(invoice.id), "method": method},
    )
    return OperationResult(instance=report, created=True)


@transaction.atomic
def confirm_payment(
    *, actor, confirmation_id, payment_report_id, confirmed_at,
    idempotency_key, correlation_id,
):
    request_hash = hash_payload({
        "confirmation_id": str(confirmation_id),
        "payment_report_id": str(payment_report_id),
        "confirmed_at": confirmed_at.isoformat(),
    })
    existing = PaymentConfirmation.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.request_hash != request_hash:
            raise PaymentIdempotencyConflictError
        AuditEvent.objects.create(
            actor=actor,
            action="payment.confirmation_idempotent_replay",
            resource_type="payment_confirmation",
            resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS,
            source="web",
            correlation_id=correlation_id,
        )
        return OperationResult(instance=existing, created=False)

    report = (
        PaymentReport.objects.select_for_update()
        .select_related("invoice")
        .filter(pk=payment_report_id)
        .first()
    )
    if not report or report.status != PaymentReport.Status.REPORTED:
        raise PaymentNotConfirmableError
    invoice = Invoice.objects.select_for_update().prefetch_related("items").get(pk=report.invoice_id)
    if invoice.status != Invoice.Status.UNPAID:
        raise PaymentNotConfirmableError

    try:
        with transaction.atomic():
            confirmation = PaymentConfirmation.objects.create(
                id=confirmation_id,
                payment_report=report,
                confirmed_by=actor,
                confirmed_at=confirmed_at,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
            )
            CommissionMovement.objects.bulk_create([
                CommissionMovement(
                    seller=invoice.seller,
                    invoice=invoice,
                    invoice_item=item,
                    payment_confirmation=confirmation,
                    reference_type="payment_confirmation",
                    reference_id=confirmation.id,
                    movement_type=CommissionMovement.MovementType.CREDIT,
                    amount=item.unit_commission * item.quantity,
                )
                for item in invoice.items.all()
            ])
            report.status = PaymentReport.Status.CONFIRMED
            report.version += 1
            report.save(update_fields=["status", "version", "updated_at"])
            invoice.status = Invoice.Status.PAID
            invoice.version += 1
            invoice.save(update_fields=["status", "version", "updated_at"])
    except IntegrityError as error:
        existing = PaymentConfirmation.objects.filter(idempotency_key=idempotency_key).first()
        if existing and existing.request_hash == request_hash:
            return OperationResult(instance=existing, created=False)
        raise PaymentIdempotencyConflictError from error

    AuditEvent.objects.create(
        actor=actor,
        action="payment.confirmed",
        resource_type="payment_confirmation",
        resource_id=str(confirmation.id),
        result=AuditEvent.Result.SUCCESS,
        source="web",
        correlation_id=correlation_id,
        metadata={"invoice_id": str(invoice.id), "payment_report_id": str(report.id)},
    )
    AuditEvent.objects.create(
        actor=actor,
        action="commission.credited",
        resource_type="invoice",
        resource_id=str(invoice.id),
        result=AuditEvent.Result.SUCCESS,
        source="web",
        correlation_id=correlation_id,
        metadata={"movement_count": invoice.items.count()},
    )
    return OperationResult(instance=confirmation, created=True)
