from rest_framework import serializers

from .models import Delivery, Invoice, InvoiceItem


class DeliveryConfirmationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    order_id = serializers.UUIDField()
    delivered_at = serializers.DateTimeField()


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = (
            "id",
            "product_id_snapshot",
            "product_sku",
            "product_name",
            "unit_price",
            "unit_commission",
            "quantity",
            "line_total",
        )
        read_only_fields = fields


class InvoiceSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    delivery_id = serializers.UUIDField(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "order_id",
            "delivery_id",
            "customer_id_snapshot",
            "customer_name",
            "customer_email",
            "customer_phone",
            "status",
            "total",
            "version",
            "issued_at",
            "updated_at",
            "items",
        )
        read_only_fields = fields


class DeliverySerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ("id", "order_id", "delivered_at", "created_at", "invoice")
        read_only_fields = fields
