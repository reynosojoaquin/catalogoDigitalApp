import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import Device, UserProfile
from audit.models import AuditEvent
from catalog.models import Customer, Product

from .models import Order


class OrderApiTests(APITestCase):
    url = "/api/orders/"

    def setUp(self):
        self.seller = self.create_seller("seller")
        self.device = Device.objects.create(
            user=self.seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )
        self.customer = Customer.objects.create(
            full_name="Customer",
            email="customer@example.test",
            created_by=self.seller,
        )
        self.product = Product.objects.create(
            sku="PRODUCT-1",
            name="Product",
            price=Decimal("125.50"),
            commission_amount=Decimal("10.25"),
        )
        self.authenticate(self.seller)

    def create_seller(self, username):
        user = get_user_model().objects.create_user(username=username, password="StrongPassword123!")
        UserProfile.objects.create(user=user, role=UserProfile.Role.SELLER)
        return user

    def authenticate(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def payload(self, **overrides):
        payload = {
            "id": str(uuid.uuid4()),
            "customer_id": str(self.customer.id),
            "device_id": str(self.device.id),
            "client_created_at": timezone.now().isoformat(),
            "items": [{"product_id": str(self.product.id), "quantity": 2}],
        }
        payload.update(overrides)
        return payload

    def post_order(self, payload, idempotency_key=None):
        return self.client.post(
            self.url,
            payload,
            format="json",
            HTTP_IDEMPOTENCY_KEY=str(idempotency_key or uuid.uuid4()),
        )

    def test_server_calculates_totals_and_captures_product_snapshots(self):
        payload = self.payload()
        payload["items"][0]["unit_price"] = "0.01"

        response = self.post_order(payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["id"], payload["id"])
        self.assertEqual(response.data["total"], "251.00")
        self.assertEqual(response.data["items"][0]["unit_price"], "125.50")
        self.assertEqual(response.data["items"][0]["unit_commission"], "10.25")
        self.assertTrue(
            AuditEvent.objects.filter(
                actor=self.seller,
                action="order.created",
                resource_id=payload["id"],
            ).exists()
        )

    def test_same_request_and_idempotency_key_returns_existing_order(self):
        payload = self.payload()
        idempotency_key = uuid.uuid4()

        first = self.post_order(payload, idempotency_key)
        second = self.post_order(payload, idempotency_key)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.data["id"], second.data["id"])
        self.assertEqual(Order.objects.count(), 1)

    def test_changed_request_with_same_idempotency_key_is_rejected(self):
        payload = self.payload()
        idempotency_key = uuid.uuid4()
        self.post_order(payload, idempotency_key)
        changed_payload = {**payload, "items": [{"product_id": str(self.product.id), "quantity": 3}]}

        response = self.post_order(changed_payload, idempotency_key)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Order.objects.count(), 1)

    def test_idempotency_header_is_required(self):
        response = self.client.post(self.url, self.payload(), format="json")

        self.assertEqual(response.status_code, 400)

    def test_seller_only_sees_own_orders(self):
        self.post_order(self.payload())
        other_seller = self.create_seller("other-seller")
        self.client.credentials()
        self.authenticate(other_seller)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_device_owned_by_another_seller_is_rejected(self):
        other_seller = self.create_seller("other-seller")
        other_device = Device.objects.create(
            user=other_seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )

        response = self.post_order(self.payload(device_id=str(other_device.id)))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(Order.objects.count(), 0)

    def test_inactive_product_is_rejected(self):
        self.product.is_active = False
        self.product.save()

        response = self.post_order(self.payload())

        self.assertEqual(response.status_code, 422)

    def test_product_changes_do_not_modify_order_snapshot(self):
        response = self.post_order(self.payload())
        order = Order.objects.get(pk=response.data["id"])
        self.product.price = Decimal("999.99")
        self.product.commission_amount = Decimal("99.99")
        self.product.save()

        item = order.items.get()

        self.assertEqual(item.unit_price, Decimal("125.50"))
        self.assertEqual(item.unit_commission, Decimal("10.25"))
        self.assertEqual(order.total, Decimal("251.00"))

    def test_duplicate_product_lines_are_rejected(self):
        duplicate_item = {"product_id": str(self.product.id), "quantity": 1}
        payload = self.payload(items=[duplicate_item, duplicate_item])

        response = self.post_order(payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_database_rejects_negative_order_total(self):
        response = self.post_order(self.payload())

        with self.assertRaises(IntegrityError), transaction.atomic():
            Order.objects.filter(pk=response.data["id"]).update(total=Decimal("-0.01"))
