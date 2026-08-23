import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import UserProfile
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

    def test_dashboard_denies_sellers(self):
        user = get_user_model().objects.create_user(username="dashboard-seller", password="A-secure-password-123")
        UserProfile.objects.create(user=user, role=UserProfile.Role.SELLER)
        self.client.force_login(user)

        self.assertEqual(self.client.get("/dashboard/").status_code, 403)

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
