from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from catalog.services import fingerprint_identity_document, normalize_email, normalize_phone
from sales.serializers import OrderItemInputSerializer

from .models import SyncDeviceCursor, SyncOperationReceipt


class SyncCustomerDataSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=30)
    identity_document = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        identifiers = (
            normalize_email(attrs.get("email")), normalize_phone(attrs.get("phone")),
            fingerprint_identity_document(attrs.get("identity_document")),
        )
        if not any(identifiers):
            raise serializers.ValidationError(_("At least one customer identifier is required."))
        return attrs


class SyncCustomerOperationSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    device_id = serializers.UUIDField()
    idempotency_key = serializers.UUIDField()
    client_timestamp = serializers.DateTimeField()
    client_version = serializers.IntegerField(min_value=1)
    customer = SyncCustomerDataSerializer()

    def validate_client_version(self, value):
        if value != 1:
            raise serializers.ValidationError(_("A new offline customer must start at version 1."))
        return value


class SyncReceiptSerializer(serializers.ModelSerializer):
    device_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = SyncOperationReceipt
        fields = (
            "operation_id", "device_id", "entity_type", "client_timestamp", "client_version",
            "status", "entity_id", "conflict_code", "server_timestamp",
        )
        read_only_fields = fields


class CursorAcknowledgementSerializer(serializers.Serializer):
    device_id = serializers.UUIDField()
    sequence = serializers.IntegerField(min_value=0)


class SyncCursorSerializer(serializers.ModelSerializer):
    device_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = SyncDeviceCursor
        fields = ("device_id", "last_sequence", "acknowledged_at")
        read_only_fields = fields


class SyncOrderDataSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_id = serializers.UUIDField()
    client_created_at = serializers.DateTimeField()
    items = OrderItemInputSerializer(many=True, allow_empty=False)

    def validate_items(self, items):
        product_ids = [item["product_id"] for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(_("Each product can appear only once per order."))
        return items


class SyncBatchOperationSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    operation_type = serializers.ChoiceField(choices=(
        "customer_create", "order_create", "payment_create", "return_create",
    ))
    idempotency_key = serializers.UUIDField()
    client_timestamp = serializers.DateTimeField()
    client_version = serializers.IntegerField(min_value=1)
    payload = serializers.JSONField()


class SyncBatchSerializer(serializers.Serializer):
    device_id = serializers.UUIDField()
    operations = SyncBatchOperationSerializer(many=True, allow_empty=False, max_length=50)

    def validate_operations(self, operations):
        operation_ids = [item["operation_id"] for item in operations]
        idempotency_keys = [item["idempotency_key"] for item in operations]
        if len(operation_ids) != len(set(operation_ids)):
            raise serializers.ValidationError(_("Operation IDs must be unique within a batch."))
        if len(idempotency_keys) != len(set(idempotency_keys)):
            raise serializers.ValidationError(_("Idempotency keys must be unique within a batch."))
        return operations
