import hashlib
import json

from django.db import transaction

from catalog.models import Customer, Product
from catalog.services import (
    DuplicateCustomerError, create_customer, fingerprint_identity_document,
    normalize_email, normalize_phone,
)
from sales.services import IdempotencyConflictError, InvalidOrderReferenceError, create_order

from .models import SyncOperationReceipt


class SyncIdempotencyConflictError(Exception):
    pass


def operation_request_hash(payload):
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()


def find_replayed_receipt(*, actor, operation_id, idempotency_key, request_hash):
    existing = SyncOperationReceipt.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.seller_id != actor.pk or existing.request_hash != request_hash:
            raise SyncIdempotencyConflictError
        return existing
    if SyncOperationReceipt.objects.filter(operation_id=operation_id).exists():
        raise SyncIdempotencyConflictError
    return None


def customer_request_hash(*, operation_id, customer_id, full_name, email, phone, identity_document, client_timestamp, client_version):
    payload = {
        "operation_id": str(operation_id),
        "customer_id": str(customer_id),
        "full_name": " ".join(full_name.split()),
        "email": normalize_email(email),
        "phone": normalize_phone(phone),
        "identity_document_hash": fingerprint_identity_document(identity_document),
        "client_timestamp": client_timestamp.isoformat(),
        "client_version": client_version,
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def sync_customer_create(
    *, actor, device, operation_id, idempotency_key, client_timestamp, client_version,
    customer_id, full_name, email, phone, identity_document, correlation_id,
):
    request_hash = customer_request_hash(
        operation_id=operation_id, customer_id=customer_id, full_name=full_name,
        email=email, phone=phone, identity_document=identity_document,
        client_timestamp=client_timestamp, client_version=client_version,
    )
    existing = SyncOperationReceipt.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.seller_id != actor.pk or existing.request_hash != request_hash:
            raise SyncIdempotencyConflictError
        return existing, False
    if SyncOperationReceipt.objects.filter(operation_id=operation_id).exists():
        raise SyncIdempotencyConflictError

    try:
        customer = create_customer(
            actor=actor, customer_id=customer_id, full_name=full_name, email=email, phone=phone,
            identity_document=identity_document, correlation_id=correlation_id,
        )
    except DuplicateCustomerError:
        receipt = SyncOperationReceipt.objects.create(
            operation_id=operation_id, seller=actor, device=device, entity_type="customer",
            idempotency_key=idempotency_key, request_hash=request_hash,
            client_timestamp=client_timestamp, client_version=client_version,
            status=SyncOperationReceipt.Status.CONFLICT, entity_id=customer_id,
            conflict_code="duplicate_customer",
        )
        return receipt, True

    receipt = SyncOperationReceipt.objects.create(
        operation_id=operation_id, seller=actor, device=device, entity_type="customer",
        idempotency_key=idempotency_key, request_hash=request_hash,
        client_timestamp=client_timestamp, client_version=client_version,
        status=SyncOperationReceipt.Status.APPLIED, entity_id=customer.id,
    )
    return receipt, True


@transaction.atomic
def sync_order_create(
    *, actor, device, operation_id, idempotency_key, client_timestamp, client_version,
    order_id, customer_id, client_created_at, items, correlation_id,
):
    request_hash = operation_request_hash({
        "operation_id": operation_id, "operation_type": "order_create",
        "client_timestamp": client_timestamp, "client_version": client_version,
        "order_id": order_id, "customer_id": customer_id,
        "client_created_at": client_created_at, "items": items,
    })
    replay = find_replayed_receipt(
        actor=actor, operation_id=operation_id, idempotency_key=idempotency_key,
        request_hash=request_hash,
    )
    if replay:
        return replay, False
    try:
        result = create_order(
            actor=actor, order_id=order_id, customer_id=customer_id, device_id=device.id,
            client_created_at=client_created_at, idempotency_key=idempotency_key,
            items=items, correlation_id=correlation_id,
        )
    except InvalidOrderReferenceError:
        receipt = SyncOperationReceipt.objects.create(
            operation_id=operation_id, seller=actor, device=device, entity_type="order",
            idempotency_key=idempotency_key, request_hash=request_hash,
            client_timestamp=client_timestamp, client_version=client_version,
            status=SyncOperationReceipt.Status.CONFLICT, entity_id=order_id,
            conflict_code="invalid_order_reference",
        )
        return receipt, True
    except IdempotencyConflictError:
        receipt = SyncOperationReceipt.objects.create(
            operation_id=operation_id, seller=actor, device=device, entity_type="order",
            idempotency_key=idempotency_key, request_hash=request_hash,
            client_timestamp=client_timestamp, client_version=client_version,
            status=SyncOperationReceipt.Status.CONFLICT, entity_id=order_id,
            conflict_code="order_idempotency_conflict",
        )
        return receipt, True
    receipt = SyncOperationReceipt.objects.create(
        operation_id=operation_id, seller=actor, device=device, entity_type="order",
        idempotency_key=idempotency_key, request_hash=request_hash,
        client_timestamp=client_timestamp, client_version=client_version,
        status=SyncOperationReceipt.Status.APPLIED, entity_id=result.order.id,
    )
    return receipt, True


@transaction.atomic
def record_rejected_operation(
    *, actor, device, operation_id, operation_type, idempotency_key,
    client_timestamp, client_version, payload, conflict_code,
):
    request_hash = operation_request_hash({
        "operation_id": operation_id, "operation_type": operation_type,
        "client_timestamp": client_timestamp, "client_version": client_version,
        "payload": payload,
    })
    replay = find_replayed_receipt(
        actor=actor, operation_id=operation_id, idempotency_key=idempotency_key,
        request_hash=request_hash,
    )
    if replay:
        return replay, False
    receipt = SyncOperationReceipt.objects.create(
        operation_id=operation_id, seller=actor, device=device,
        entity_type=operation_type.removesuffix("_create"),
        idempotency_key=idempotency_key, request_hash=request_hash,
        client_timestamp=client_timestamp, client_version=client_version,
        status=SyncOperationReceipt.Status.REJECTED, conflict_code=conflict_code,
    )
    return receipt, True


def serialize_change(change):
    if change.entity_type == "customer":
        entity = Customer.objects.filter(pk=change.entity_id).first()
        data = None if entity is None else {
            "id": str(entity.id), "full_name": entity.full_name, "email": entity.email,
            "phone": entity.phone, "is_active": entity.is_active, "version": entity.version,
            "updated_at": entity.updated_at.isoformat(),
        }
    else:
        entity = Product.objects.filter(pk=change.entity_id).first()
        data = None if entity is None else {
            "id": str(entity.id), "sku": entity.sku, "name": entity.name,
            "description": entity.description, "price": str(entity.price),
            "commission_amount": str(entity.commission_amount), "is_active": entity.is_active,
            "version": entity.version, "updated_at": entity.updated_at.isoformat(),
        }
    return {
        "sequence": change.sequence, "entity_type": change.entity_type,
        "entity_id": str(change.entity_id), "version": change.version,
        "occurred_at": change.occurred_at.isoformat(), "data": data,
    }
