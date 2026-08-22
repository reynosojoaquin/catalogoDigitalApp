import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("occurred_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("action", models.CharField(db_index=True, max_length=120)),
                ("resource_type", models.CharField(blank=True, db_index=True, max_length=100)),
                ("resource_id", models.CharField(blank=True, db_index=True, max_length=100)),
                ("result", models.CharField(choices=[("success", "Success"), ("denied", "Denied"), ("failure", "Failure")], db_index=True, max_length=10)),
                ("source", models.CharField(default="web", max_length=20)),
                ("correlation_id", models.UUIDField(db_index=True)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-occurred_at"],
                "indexes": [models.Index(fields=["resource_type", "resource_id", "occurred_at"], name="audit_audit_resourc_3f6b4f_idx")],
            },
        ),
    ]
