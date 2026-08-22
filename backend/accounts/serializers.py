from rest_framework import serializers

from .models import Device


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Device
        fields = ("id", "platform", "app_version")


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "platform",
            "app_version",
            "is_active",
            "registered_at",
            "last_seen_at",
        )
        read_only_fields = fields
