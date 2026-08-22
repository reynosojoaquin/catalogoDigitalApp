from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import ReturnConfirmation, ReturnItem, ReturnReport


class ReturnItemInputSerializer(serializers.Serializer):
    invoice_item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class ReturnReportCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    invoice_id = serializers.UUIDField()
    device_id = serializers.UUIDField()
    client_reported_at = serializers.DateTimeField()
    items = ReturnItemInputSerializer(many=True, allow_empty=False)

    def validate_items(self, items):
        item_ids = [item["invoice_item_id"] for item in items]
        if len(item_ids) != len(set(item_ids)):
            raise serializers.ValidationError(_("Each invoice item can appear only once per return."))
        return items


class ReturnItemSerializer(serializers.ModelSerializer):
    invoice_item_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = ReturnItem
        fields = (
            "id", "invoice_item_id", "quantity", "unit_price", "unit_commission",
            "line_total", "commission_total",
        )
        read_only_fields = fields


class ReturnReportSerializer(serializers.ModelSerializer):
    invoice_id = serializers.UUIDField(read_only=True)
    device_id = serializers.UUIDField(read_only=True)
    items = ReturnItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReturnReport
        fields = (
            "id", "invoice_id", "device_id", "status", "total", "commission_total",
            "version", "client_reported_at", "created_at", "updated_at", "items",
        )
        read_only_fields = fields


class ReturnConfirmationCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    return_report_id = serializers.UUIDField()
    confirmed_at = serializers.DateTimeField()


class ReturnConfirmationSerializer(serializers.ModelSerializer):
    return_report_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = ReturnConfirmation
        fields = ("id", "return_report_id", "confirmed_at", "created_at")
        read_only_fields = fields
