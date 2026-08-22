import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from audit.models import AuditEvent

from .models import Device, UserProfile


class DeviceRegistrationApiTests(APITestCase):
    url = "/api/devices/register/"

    def create_user(self, username, role):
        user = get_user_model().objects.create_user(username=username, password="StrongPassword123!")
        UserProfile.objects.create(user=user, role=role)
        return user

    def authenticate(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def payload(self, device_id=None):
        return {
            "id": str(device_id or uuid.uuid4()),
            "platform": Device.Platform.ANDROID,
            "app_version": "1.0.0",
        }

    def test_anonymous_user_is_denied(self):
        response = self.client.post(self.url, self.payload(), format="json")

        self.assertEqual(response.status_code, 401)

    def test_non_seller_is_denied(self):
        user = self.create_user("admin", UserProfile.Role.ADMIN)
        self.authenticate(user)

        response = self.client.post(self.url, self.payload(), format="json")

        self.assertEqual(response.status_code, 403)

    def test_seller_can_register_device_and_action_is_audited(self):
        seller = self.create_user("seller", UserProfile.Role.SELLER)
        self.authenticate(seller)

        response = self.client.post(self.url, self.payload(), format="json")

        self.assertEqual(response.status_code, 201)
        device = Device.objects.get(pk=response.data["id"])
        self.assertEqual(device.user, seller)
        self.assertTrue(
            AuditEvent.objects.filter(
                actor=seller,
                action="device.registered",
                resource_id=str(device.id),
            ).exists()
        )

    def test_same_seller_can_refresh_device_registration(self):
        seller = self.create_user("seller", UserProfile.Role.SELLER)
        self.authenticate(seller)
        device_id = uuid.uuid4()
        self.client.post(self.url, self.payload(device_id), format="json")

        payload = self.payload(device_id)
        payload["app_version"] = "1.1.0"
        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Device.objects.get(pk=device_id).app_version, "1.1.0")
        self.assertEqual(Device.objects.filter(pk=device_id).count(), 1)

    def test_device_cannot_be_claimed_by_another_seller(self):
        first_seller = self.create_user("seller-one", UserProfile.Role.SELLER)
        second_seller = self.create_user("seller-two", UserProfile.Role.SELLER)
        device_id = uuid.uuid4()
        Device.objects.create(
            id=device_id,
            user=first_seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )
        self.authenticate(second_seller)

        response = self.client.post(self.url, self.payload(device_id), format="json")

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Device.objects.get(pk=device_id).user, first_seller)


class AuthenticationAuditTests(APITestCase):
    url = "/api/auth/token/"

    def test_successful_authentication_is_audited(self):
        user = get_user_model().objects.create_user(
            username="seller",
            password="StrongPassword123!",
        )

        response = self.client.post(
            self.url,
            {"username": "seller", "password": "StrongPassword123!"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertTrue(
            AuditEvent.objects.filter(
                actor=user,
                action="authentication.login",
                result=AuditEvent.Result.SUCCESS,
            ).exists()
        )

    def test_failed_authentication_is_audited_without_credentials(self):
        response = self.client.post(
            self.url,
            {"username": "unknown", "password": "not-recorded"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        event = AuditEvent.objects.get(
            action="authentication.login",
            result=AuditEvent.Result.DENIED,
        )
        self.assertEqual(event.metadata, {})
        self.assertIsNone(event.actor)

    def test_repeated_login_attempts_are_throttled_and_audited_without_credentials(self):
        from rest_framework.throttling import ScopedRateThrottle

        cache.clear()
        payload = {"username": "unknown", "password": "never-recorded"}

        with patch.object(ScopedRateThrottle, "THROTTLE_RATES", {"login": "2/min"}):
            first = self.client.post(self.url, payload, format="json", REMOTE_ADDR="198.51.100.20")
            second = self.client.post(self.url, payload, format="json", REMOTE_ADDR="198.51.100.20")
            third = self.client.post(self.url, payload, format="json", REMOTE_ADDR="198.51.100.20")

        self.assertEqual(first.status_code, 400)
        self.assertEqual(second.status_code, 400)
        self.assertEqual(third.status_code, 429)
        event = AuditEvent.objects.get(action="authentication.throttled")
        self.assertEqual(event.metadata, {})
        self.assertEqual(event.ip_address, "198.51.100.20")
        cache.clear()
