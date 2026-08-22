import hashlib
import json
from dataclasses import dataclass

from django.db import IntegrityError, transaction

from audit.models import AuditEvent
from sales.models import Order

from .models import Delivery, Invoice, InvoiceItem


class DeliveryIdempotencyConflictError(Exception):
    pass


class OrderNotDeliverableError(Exception):
    pass


@dataclass(frozen=True)
class DeliveryConfirmationResult:
    delivery: Delivery
    invoice: Invoice
    created: bool


def build_delivery_request_hash(*, delivery_id, order_id, delivered_at):
    payload = {
        "delivery_id": str(delivery_id),
        "order_id": str(order_id),
        "delivered_at": delivered_at.isoformat(),
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def confirm_complete_delivery(
    *,
    actor,
    delivery_id,
    order_id,
    delivered_at,
    idempotency_key,
    correlation_id,
):
    request_hash = build_delivery_request_hash(
        delivery_id=delivery_id,
        order_id=order_id,
        delivered_at=delivered_at,
    )
    existing = Delivery.objects.select_related("invoice").filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.request_hash != request_hash:
            raise DeliveryIdempotencyConflictError
        AuditEvent.objects.create(
            actor=actor,
            action="delivery.idempotent_replay",
            resource_type="delivery",
            resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS,
            source="web",
            correlation_id=correlation_id,
        )
        return DeliveryConfirmationResult(delivery=existing, invoice=existing.invoice, created=False)

    order = (
        Order.objects.select_for_update()
        .select_related("customer", "seller")
        .prefetch_related("items")
        .filter(pk=order_id)
        .first()
    )
    if not order or order.status != Order.Status.SUBMITTED:
        raise OrderNotDeliverableError

    try:
        with transaction.atomic():
            delivery = Delivery.objects.create(
                id=delivery_id,
                order=order,
                confirmed_by=actor,
                delivered_at=delivered_at,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
            )
            invoice = Invoice.objects.create(
                delivery=delivery,
                order=order,
                seller=order.seller,
                customer_id_snapshot=order.customer_id,
                customer_name=order.customer.full_name,
                customer_email=order.customer.email,
                customer_phone=order.customer.phone,
                total=order.total,
            )
            InvoiceItem.objects.bulk_create([
                InvoiceItem(
                    invoice=invoice,
                    order_item=item,
                    product_id_snapshot=item.product_id,
                    product_sku=item.product_sku,
                    product_name=item.product_name,
                    unit_price=item.unit_price,
                    unit_commission=item.unit_commission,
                    quantity=item.quantity,
                    line_total=item.line_total,
                )
                for item in order.items.all()
            ])
            order.status = Order.Status.DELIVERED
            order.version += 1
            order.save(update_fields=["status", "version", "updated_at"])
    except IntegrityError as error:
        existing = Delivery.objects.select_related("invoice").filter(idempotency_key=idempotency_key).first()
        if existing and existing.request_hash == request_hash:
            return DeliveryConfirmationResult(delivery=existing, invoice=existing.invoice, created=False)
        raise DeliveryIdempotencyConflictError from error

    AuditEvent.objects.create(
        actor=actor,
        action="delivery.completed",
        resource_type="delivery",
        resource_id=str(delivery.id),
        result=AuditEvent.Result.SUCCESS,
        source="web",
        correlation_id=correlation_id,
        metadata={"order_id": str(order.id), "invoice_id": str(invoice.id)},
    )
    AuditEvent.objects.create(
        actor=actor,
        action="invoice.issued",
        resource_type="invoice",
        resource_id=str(invoice.id),
        result=AuditEvent.Result.SUCCESS,
        source="web",
        correlation_id=correlation_id,
        metadata={"order_id": str(order.id)},
    )
    return DeliveryConfirmationResult(delivery=delivery, invoice=invoice, created=True)
