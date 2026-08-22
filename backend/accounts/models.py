import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", _("Administrator")
        SELLER = "seller", _("Seller")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=Role.choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_id}:{self.role}"


class Device(models.Model):
    class Platform(models.TextChoices):
        ANDROID = "android", _("Android")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="devices",
    )
    platform = models.CharField(max_length=20, choices=Platform.choices)
    app_version = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True, db_index=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_seen_at"]

    def __str__(self):
        return str(self.id)
