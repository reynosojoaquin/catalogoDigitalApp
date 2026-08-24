import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import UserProfile
from accounts.models import Device
from catalog.models import Product


class HealthEndpointTests(TestCase):
    def test_health_endpoint_is_public_and_checks_database_and_cache(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_endpoint_returns_correlation_id(self):
        correlation_id = uuid.uuid4()

        response = self.client.get("/health/", headers={"X-Correlation-ID": str(correlation_id)})

        self.assertEqual(response.headers["X-Correlation-ID"], str(correlation_id))

    def test_invalid_correlation_id_is_replaced(self):
        response = self.client.get("/health/", headers={"X-Correlation-ID": "invalid"})

        uuid.UUID(response.headers["X-Correlation-ID"])


class DashboardTests(TestCase):
    def test_dashboard_requires_authentication(self):
        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_dashboard_is_available_to_administrator(self):
        user = get_user_model().objects.create_user(username="dashboard-admin", password="A-secure-password-123")
        UserProfile.objects.create(user=user, role=UserProfile.Role.ADMIN)
        self.client.force_login(user)

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Administration dashboard")
        self.assertContains(response, 'href="/app/catalog/"')

    def test_dashboard_denies_sellers(self):
        user = get_user_model().objects.create_user(username="dashboard-seller", password="A-secure-password-123")
        UserProfile.objects.create(user=user, role=UserProfile.Role.SELLER)
        self.client.force_login(user)

        self.assertEqual(self.client.get("/dashboard/").status_code, 403)

    def test_language_switcher_uses_spanish_catalog(self):
        user = get_user_model().objects.create_superuser(username="language-admin", password="A-secure-password-123")
        self.client.force_login(user)
        switch = self.client.post("/i18n/setlang/", {"language": "es-do", "next": "/dashboard/"})

        self.assertEqual(switch.status_code, 302)
        response = self.client.get("/dashboard/")

        self.assertContains(response, "Panel principal")

    def test_custom_resource_view_renders_real_catalog_records_and_searches(self):
        user = get_user_model().objects.create_superuser(username="resource-admin", password="A-secure-password-123")
        Product.objects.create(sku="SKU-001", name="Visible product", price="10.00", commission_amount="1.00")
        Product.objects.create(sku="SKU-002", name="Other product", price="20.00", commission_amount="2.00")
        self.client.force_login(user)

        response = self.client.get("/app/catalog/?q=Visible")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible product")
        self.assertNotContains(response, "Other product")

    def test_custom_resource_view_denies_non_administrator(self):
        user = get_user_model().objects.create_user(username="resource-seller", password="A-secure-password-123")
        UserProfile.objects.create(user=user, role=UserProfile.Role.SELLER)
        self.client.force_login(user)

        self.assertEqual(self.client.get("/app/orders/").status_code, 403)

    def test_custom_resource_detail_renders_record(self):
        user = get_user_model().objects.create_superuser(username="detail-admin", password="A-secure-password-123")
        product = Product.objects.create(sku="SKU-DETAIL", name="Detailed product", price="12.50", commission_amount="1.25")
        self.client.force_login(user)

        response = self.client.get(f"/app/catalog/{product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detailed product")

    def test_devices_view_renders_without_sensitive_session_data(self):
        user = get_user_model().objects.create_superuser(username="device-admin", password="A-secure-password-123")
        seller = get_user_model().objects.create_user(username="seller-one", password="A-secure-password-123")
        device = Device.objects.create(user=seller, platform=Device.Platform.ANDROID, app_version="1.0.0")
        self.client.force_login(user)

        response = self.client.get("/app/devices/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(device.id))
        self.assertNotContains(response, "A-secure-password-123")
