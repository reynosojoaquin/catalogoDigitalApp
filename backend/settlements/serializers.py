from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CommissionSettlement, CommissionSettlementItem


class SettlementConfirmationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    seller_id = serializers.IntegerField(min_value=1)
    period_ends_at = serializers.DateTimeField()
    confirmed_at = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs["period_ends_at"] > attrs["confirmed_at"]:
            raise serializers.ValidationError({
                "period_ends_at": _("The period end cannot be later than confirmation time.")
            })
        return attrs


class SettlementItemSerializer(serializers.ModelSerializer):
    movement_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = CommissionSettlementItem
        fields = ("id", "movement_id", "movement_type", "amount", "signed_amount")
        read_only_fields = fields


class SettlementSerializer(serializers.ModelSerializer):
    items = SettlementItemSerializer(many=True, read_only=True)

    class Meta:
        model = CommissionSettlement
        fields = ("id", "period_ends_at", "total", "confirmed_at", "created_at", "items")
        read_only_fields = fields
