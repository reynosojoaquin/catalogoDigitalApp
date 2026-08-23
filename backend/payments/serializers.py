import re

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CommissionMovement, PaymentConfirmation, PaymentReport


def looks_like_card_number(value):
    candidate = value.strip()
    if not re.fullmatch(r"[0-9][0-9 -]*", candidate):
        return False
    digits = "".join(character for character in candidate if character.isdigit())
    return 13 <= len(digits) <= 19


class PaymentReportCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    invoice_id = serializers.UUIDField()
    device_id = serializers.UUIDField()
    method = serializers.ChoiceField(choices=PaymentReport.Method.choices)
    external_terminal_reference = serializers.CharField(required=False, allow_blank=True, max_length=120)
    client_reported_at = serializers.DateTimeField()

    def validate(self, attrs):
        reference = attrs.get("external_terminal_reference", "").strip() or None
        if attrs["method"] == PaymentReport.Method.EXTERNAL_CARD_TERMINAL and not reference:
            raise serializers.ValidationError({
                "external_terminal_reference": _("A terminal reference is required for card payments.")
            })
        if attrs["method"] == PaymentReport.Method.CASH and reference:
            raise serializers.ValidationError({
                "external_terminal_reference": _("Cash payments cannot include a terminal reference.")
            })
        if reference and looks_like_card_number(reference):
            raise serializers.ValidationError({
                "external_terminal_reference": _("Card numbers cannot be stored as terminal references.")
            })
        attrs["external_terminal_reference"] = reference
        return attrs


class PaymentConfirmationCreateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    payment_report_id = serializers.UUIDField()
    confirmed_at = serializers.DateTimeField()


class PaymentReportSerializer(serializers.ModelSerializer):
    invoice_id = serializers.UUIDField(read_only=True)
    device_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PaymentReport
        fields = (
            "id", "invoice_id", "device_id", "method", "external_terminal_reference",
            "amount", "status", "version", "client_reported_at", "created_at", "updated_at",
        )
        read_only_fields = fields


class PaymentConfirmationSerializer(serializers.ModelSerializer):
    payment_report_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = PaymentConfirmation
        fields = ("id", "payment_report_id", "confirmed_at", "created_at")
        read_only_fields = fields


class CommissionMovementSerializer(serializers.ModelSerializer):
    invoice_id = serializers.UUIDField(read_only=True)
    invoice_item_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = CommissionMovement
        fields = (
            "id", "invoice_id", "invoice_item_id", "movement_type", "amount", "status", "version", "created_at",
        )
        read_only_fields = fields
