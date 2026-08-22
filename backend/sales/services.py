import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal

from django.db import IntegrityError, transaction

from accounts.models import Device
from audit.models import AuditEvent
from catalog.models import Customer, Product

from .models import Order, OrderItem


class IdempotencyConflictError(Exception):
    pass


class InvalidOrderReferenceError(Exception):
    pass


@dataclass(frozen=True)
class OrderCreationResult:
    order: Order
    created: bool


def build_request_hash(*, order_id, customer_id, device_id, client_created_at, items):
    payload = {
        "order_id": str(order_id),
        "customer_id": str(customer_id),
        "device_id": str(device_id),
        "client_created_at": client_created_at.isoformat(),
        "items": sorted(
            ({"product_id": str(item["product_id"]), "quantity": item["quantity"]} for item in items),
            key=lambda item: item["product_id"],
        ),
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def create_order(
    *,
    actor,
    order_id,
    customer_id,
    device_id,
    client_created_at,
    idempotency_key,
    items,
    correlation_id,
):
    request_hash = build_request_hash(
        order_id=order_id,
        customer_id=customer_id,
        device_id=device_id,
        client_created_at=client_created_at,
        items=items,
    )
    existing = Order.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.seller_id != actor.pk or existing.request_hash != request_hash:
            raise IdempotencyConflictError
        AuditEvent.objects.create(
            actor=actor,
            action="order.idempotent_replay",
            resource_type="order",
            resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS,
            source="android",
            correlation_id=correlation_id,
        )
        return OrderCreationResult(order=existing, created=False)

    customer = Customer.objects.filter(pk=customer_id, is_active=True).first()
    device = Device.objects.filter(pk=device_id, user=actor, is_active=True).first()
    product_ids = [item["product_id"] for item in items]
    products = Product.objects.filter(pk__in=product_ids, is_active=True).in_bulk()
    if not customer or not device or len(products) != len(product_ids):
        raise InvalidOrderReferenceError

    item_models = []
    total = Decimal("0.00")
    for item in items:
        product = products[item["product_id"]]
        line_total = product.price * item["quantity"]
        total += line_total
        item_models.append(
            OrderItem(
                product=product,
                product_sku=product.sku,
                product_name=product.name,
                unit_price=product.price,
                unit_commission=product.commission_amount,
                quantity=item["quantity"],
                line_total=line_total,
            )
        )

    try:
        with transaction.atomic():
            order = Order.objects.create(
                id=order_id,
                seller=actor,
                customer=customer,
                device=device,
                total=total,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                client_created_at=client_created_at,
            )
            for item_model in item_models:
                item_model.order = order
            OrderItem.objects.bulk_create(item_models)
    except IntegrityError as error:
        existing = Order.objects.filter(idempotency_key=idempotency_key).first()
        if existing and existing.seller_id == actor.pk and existing.request_hash == request_hash:
            return OrderCreationResult(order=existing, created=False)
        raise IdempotencyConflictError from error

    AuditEvent.objects.create(
        actor=actor,
        action="order.created",
        resource_type="order",
        resource_id=str(order.id),
        result=AuditEvent.Result.SUCCESS,
        source="android",
        correlation_id=correlation_id,
        metadata={"item_count": len(item_models)},
    )
    return OrderCreationResult(order=order, created=True)
