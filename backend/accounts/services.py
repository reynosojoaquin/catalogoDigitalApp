from dataclasses import dataclass

from django.db import transaction

from audit.models import AuditEvent

from .models import Device


class DeviceOwnershipError(Exception):
    pass


@dataclass(frozen=True)
class DeviceRegistrationResult:
    device: Device
    created: bool


@transaction.atomic
def register_device(*, user, device_id, platform, app_version, correlation_id):
    device = Device.objects.select_for_update().filter(pk=device_id).first()
    if device and device.user_id != user.pk:
        raise DeviceOwnershipError

    if device:
        device.platform = platform
        device.app_version = app_version
        device.is_active = True
        device.save(update_fields=["platform", "app_version", "is_active", "last_seen_at"])
        created = False
    else:
        device = Device.objects.create(
            id=device_id,
            user=user,
            platform=platform,
            app_version=app_version,
        )
        created = True

    AuditEvent.objects.create(
        actor=user,
        action="device.registered" if created else "device.refreshed",
        resource_type="device",
        resource_id=str(device.id),
        result=AuditEvent.Result.SUCCESS,
        source="android",
        correlation_id=correlation_id,
    )
    return DeviceRegistrationResult(device=device, created=created)
