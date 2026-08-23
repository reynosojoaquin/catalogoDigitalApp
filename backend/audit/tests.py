import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import UserProfile

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


class AdminMutationAuditTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="audit-admin",
            email="admin@example.invalid",
            password="StrongPassword123!",
        )
        self.client.force_login(self.admin)

    def test_admin_change_is_audited_without_form_data(self):
        response = self.client.post("/admin/auth/group/add/", {"name": "operators", "permissions": []})

        self.assertEqual(response.status_code, 302)
        event = AuditEvent.objects.get(action="admin.mutation")
        self.assertEqual(event.actor, self.admin)
        self.assertEqual(event.result, AuditEvent.Result.SUCCESS)
        self.assertEqual(event.source, "admin")
        self.assertEqual(event.metadata["method"], "POST")
        self.assertNotIn("name", event.metadata)

    def test_denied_admin_login_is_audited_without_credentials(self):
        self.client.logout()

        response = self.client.post(
            "/admin/login/",
            {"username": "unknown", "password": "not-recorded", "next": "/admin/"},
        )

        self.assertEqual(response.status_code, 200)
        event = AuditEvent.objects.get(action="admin.mutation")
        self.assertIsNone(event.actor)
        self.assertEqual(event.result, AuditEvent.Result.DENIED)
        self.assertEqual(event.metadata["path"], "/admin/login/")
        self.assertNotIn("password", event.metadata)

    def test_failed_api_mutation_is_audited_without_payload(self):
        self.client.logout()

        response = self.client.post(
            "/api/customers/",
            {"full_name": "not-stored"},
            format="json",
        )

        self.assertIn(response.status_code, (401, 403))
        event = AuditEvent.objects.get(action="api.operation_denied")
        self.assertIsNone(event.actor)
        self.assertEqual(event.metadata["path"], "/api/customers/")
        self.assertNotIn("full_name", event.metadata)

    def test_staff_seller_cannot_access_admin_models(self):
        seller = get_user_model().objects.create_user(
            username="staff-seller",
            password="StrongPassword123!",
            is_staff=True,
        )
        UserProfile.objects.create(user=seller, role=UserProfile.Role.SELLER)
        self.client.force_login(seller)

        response = self.client.get("/admin/catalog/product/")

        self.assertEqual(response.status_code, 403)

        response = self.client.get("/admin/auth/user/")

        self.assertEqual(response.status_code, 403)
