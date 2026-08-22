import uuid

from django.test import TestCase

from .models import AuditEvent


class AuditEventImmutabilityTests(TestCase):
    def setUp(self):
        self.event = AuditEvent.objects.create(
            action="test.created",
            result=AuditEvent.Result.SUCCESS,
            correlation_id=uuid.uuid4(),
        )

    def test_instance_cannot_be_updated(self):
        self.event.action = "test.changed"

        with self.assertRaisesMessage(ValueError, "append-only"):
            self.event.save()

    def test_queryset_cannot_be_updated(self):
        with self.assertRaisesMessage(ValueError, "append-only"):
            AuditEvent.objects.filter(pk=self.event.pk).update(action="test.changed")

    def test_instance_cannot_be_deleted(self):
        with self.assertRaisesMessage(ValueError, "append-only"):
            self.event.delete()

    def test_queryset_cannot_be_deleted(self):
        with self.assertRaisesMessage(ValueError, "append-only"):
            AuditEvent.objects.filter(pk=self.event.pk).delete()

