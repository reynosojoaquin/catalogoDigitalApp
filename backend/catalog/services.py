import hashlib
import hmac
import re

from django.conf import settings
from django.db import IntegrityError, transaction

from audit.models import AuditEvent

from .models import Customer


class DuplicateCustomerError(Exception):
    pass


def normalize_email(value):
    return value.strip().casefold() if value else None


def normalize_phone(value):
    if not value:
        return None
    normalized = re.sub(r"[^0-9+]", "", value.strip())
    if normalized.startswith("+"):
        normalized = "+" + normalized[1:].replace("+", "")
    else:
        normalized = normalized.replace("+", "")
    return normalized or None


def fingerprint_identity_document(value):
    if not value:
        return None
    normalized = re.sub(r"[^0-9A-Za-z]", "", value).casefold()
    if not normalized:
        return None
    return hmac.new(
        settings.PII_HASH_KEY.encode(),
        normalized.encode(),
        hashlib.sha256,
    ).hexdigest()


@transaction.atomic
def create_customer(
    *, actor, full_name, email, phone, identity_document, correlation_id, customer_id=None,
):
    normalized_email = normalize_email(email)
    normalized_phone = normalize_phone(phone)
    document_hash = fingerprint_identity_document(identity_document)

    duplicate_filters = {
        "email": normalized_email,
        "phone": normalized_phone,
        "identity_document_hash": document_hash,
    }
    for field, value in duplicate_filters.items():
        if value and Customer.objects.filter(**{field: value}).exists():
            raise DuplicateCustomerError

    try:
        customer_values = {
            "full_name": " ".join(full_name.split()),
            "email": normalized_email,
            "phone": normalized_phone,
            "identity_document_hash": document_hash,
            "created_by": actor,
        }
        if customer_id is not None:
            customer_values["id"] = customer_id
        customer = Customer.objects.create(
            **customer_values,
        )
    except IntegrityError as error:
        raise DuplicateCustomerError from error

    AuditEvent.objects.create(
        actor=actor,
        action="customer.created",
        resource_type="customer",
        resource_id=str(customer.id),
        result=AuditEvent.Result.SUCCESS,
        source="android",
        correlation_id=correlation_id,
    )
    return customer
