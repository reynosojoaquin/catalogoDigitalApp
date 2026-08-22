from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_id = serializers.UUIDField()
    device_id = serializers.UUIDField()
    client_created_at = serializers.DateTimeField()
    items = OrderItemInputSerializer(many=True, allow_empty=False)

    def validate_items(self, items):
        product_ids = [item["product_id"] for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(_("Each product can appear only once per order."))
        return items


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_id",
            "product_sku",
            "product_name",
            "unit_price",
            "unit_commission",
            "quantity",
            "line_total",
        )
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.UUIDField(read_only=True)
    device_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "customer_id",
            "device_id",
            "status",
            "total",
            "version",
            "client_created_at",
            "created_at",
            "updated_at",
            "items",
        )
        read_only_fields = fields
