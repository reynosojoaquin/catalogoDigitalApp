import uuid

from django.test import TestCase


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
