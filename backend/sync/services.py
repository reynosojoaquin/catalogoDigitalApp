import hashlib
import json

from django.db import transaction

from catalog.models import Customer, Product
from catalog.services import (
    DuplicateCustomerError, create_customer, fingerprint_identity_document,
    normalize_email, normalize_phone,
)

from .models import SyncOperationReceipt


class SyncIdempotencyConflictError(Exception):
    pass


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
