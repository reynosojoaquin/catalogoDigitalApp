from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Customer, Product
from .services import fingerprint_identity_document, normalize_email, normalize_phone


class CustomerSerializer(serializers.ModelSerializer):
    identity_document = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Customer
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "identity_document",
            "is_active",
            "version",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_active", "version", "created_at", "updated_at")

    def validate(self, attrs):
        identifiers = (
            normalize_email(attrs.get("email")),
            normalize_phone(attrs.get("phone")),
            fingerprint_identity_document(attrs.get("identity_document")),
        )
        if not any(identifiers):
            raise serializers.ValidationError(
                _("At least one email, phone number, or identity document is required.")
            )
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "sku",
            "name",
            "description",
            "price",
            "commission_amount",
            "version",
            "updated_at",
        )
        read_only_fields = fields
