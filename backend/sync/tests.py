import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import Device, UserProfile
from catalog.models import Customer, Product
from sales.models import Order

from .models import SyncChange, SyncDeviceCursor, SyncOperationReceipt


class OfflineSyncApiTests(APITestCase):
    operation_url = "/api/sync/customer-operations/"
    changes_url = "/api/sync/catalog-changes/"
    cursor_url = "/api/sync/cursor/ack/"
    batch_url = "/api/sync/batch/"

    def setUp(self):
        self.seller = get_user_model().objects.create_user(
            username="seller", password="StrongPassword123!"
        )
        UserProfile.objects.create(user=self.seller, role=UserProfile.Role.SELLER)
        self.device = Device.objects.create(
            user=self.seller, platform=Device.Platform.ANDROID, app_version="1.0.0"
        )
        token = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def operation_payload(self, **overrides):
        customer = {
            "id": str(uuid.uuid4()),
            "full_name": "Offline Customer",
            "email": "offline@example.test",
            "identity_document": "document-value",
        }
        payload = {
            "operation_id": str(uuid.uuid4()),
            "device_id": str(self.device.id),
            "idempotency_key": str(uuid.uuid4()),
            "client_timestamp": timezone.now().isoformat(),
            "client_version": 1,
            "customer": customer,
        }
        payload.update(overrides)
        return payload

    def test_customer_uuid_is_preserved_and_receipt_has_no_sensitive_payload(self):
        payload = self.operation_payload()

        response = self.client.post(self.operation_url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], SyncOperationReceipt.Status.APPLIED)
        self.assertEqual(response.data["entity_id"], payload["customer"]["id"])
        customer = Customer.objects.get(pk=payload["customer"]["id"])
        self.assertNotEqual(customer.identity_document_hash, payload["customer"]["identity_document"])
        receipt = SyncOperationReceipt.objects.get(operation_id=payload["operation_id"])
        self.assertFalse(hasattr(receipt, "payload"))
        self.assertNotIn("identity_document", response.data)

    def test_identical_retry_returns_existing_receipt(self):
        payload = self.operation_payload()

        first = self.client.post(self.operation_url, payload, format="json")
        second = self.client.post(self.operation_url, payload, format="json")

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(SyncOperationReceipt.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)

    def test_reused_idempotency_key_with_changed_operation_is_explicit_conflict(self):
        payload = self.operation_payload()
        self.client.post(self.operation_url, payload, format="json")
        changed = {**payload, "operation_id": str(uuid.uuid4())}

        response = self.client.post(self.operation_url, changed, format="json")

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Customer.objects.count(), 1)

    def test_new_customer_rejects_non_initial_client_version(self):
        payload = self.operation_payload(client_version=2)

        response = self.client.post(self.operation_url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Customer.objects.exists())

    def test_duplicate_customer_creates_durable_conflict_receipt(self):
        Customer.objects.create(
            full_name="Existing", email="offline@example.test", created_by=self.seller
        )
        payload = self.operation_payload()

        response = self.client.post(self.operation_url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], SyncOperationReceipt.Status.CONFLICT)
        self.assertEqual(response.data["conflict_code"], "duplicate_customer")
        self.assertEqual(Customer.objects.count(), 1)

    def test_catalog_feed_is_incremental_and_uses_server_versions(self):
        product = Product.objects.create(
            sku="PRODUCT-1", name="Product", price=Decimal("100.00"),
            commission_amount=Decimal("5.00"),
        )
        first_sequence = SyncChange.objects.get(entity_type="product", version=1).sequence
        product.price = Decimal("125.00")
        product.save()

        response = self.client.get(self.changes_url, {"after": first_sequence})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["changes"]), 1)
        change = response.data["changes"][0]
        self.assertEqual(change["version"], 2)
        self.assertEqual(change["data"]["price"], "125.00")
        self.assertEqual(response.data["next_cursor"], change["sequence"])

    def test_cursor_acknowledgement_is_monotonic_and_device_scoped(self):
        Product.objects.create(
            sku="PRODUCT-1", name="Product", price=Decimal("100.00"),
            commission_amount=Decimal("5.00"),
        )
        sequence = SyncChange.objects.latest("sequence").sequence

        first = self.client.post(
            self.cursor_url, {"device_id": str(self.device.id), "sequence": sequence}, format="json"
        )
        backwards = self.client.post(
            self.cursor_url, {"device_id": str(self.device.id), "sequence": sequence - 1}, format="json"
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(backwards.status_code, 400)
        self.assertEqual(SyncDeviceCursor.objects.get(device=self.device).last_sequence, sequence)

    def test_batch_applies_customer_then_order_with_server_prices(self):
        product = Product.objects.create(
            sku="PRODUCT-1", name="Product", price=Decimal("125.50"),
            commission_amount=Decimal("5.00"),
        )
        customer_id = uuid.uuid4()
        operations = [
            {
                "operation_id": str(uuid.uuid4()), "operation_type": "customer_create",
                "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
                "client_version": 1,
                "payload": {"id": str(customer_id), "full_name": "Offline Customer", "email": "batch@example.test"},
            },
            {
                "operation_id": str(uuid.uuid4()), "operation_type": "order_create",
                "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
                "client_version": 1,
                "payload": {
                    "id": str(uuid.uuid4()), "customer_id": str(customer_id),
                    "client_created_at": timezone.now().isoformat(),
                    "items": [{"product_id": str(product.id), "quantity": 2, "unit_price": "0.01"}],
                },
            },
        ]

        response = self.client.post(
            self.batch_url, {"device_id": str(self.device.id), "operations": operations}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["counts"]["applied"], 2)
        order = Order.objects.get(pk=operations[1]["payload"]["id"])
        self.assertEqual(order.total, Decimal("251.00"))
        self.assertEqual(order.items.get().unit_price, Decimal("125.50"))

    def test_batch_returns_partial_results_without_rolling_back_successes(self):
        customer_operation = {
            "operation_id": str(uuid.uuid4()), "operation_type": "customer_create",
            "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
            "client_version": 1,
            "payload": {"id": str(uuid.uuid4()), "full_name": "Customer", "email": "partial@example.test"},
        }
        order_operation = {
            "operation_id": str(uuid.uuid4()), "operation_type": "order_create",
            "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
            "client_version": 1,
            "payload": {
                "id": str(uuid.uuid4()), "customer_id": customer_operation["payload"]["id"],
                "client_created_at": timezone.now().isoformat(),
                "items": [{"product_id": str(uuid.uuid4()), "quantity": 1}],
            },
        }

        response = self.client.post(
            self.batch_url,
            {"device_id": str(self.device.id), "operations": [customer_operation, order_operation]},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["counts"]["applied"], 1)
        self.assertEqual(response.data["counts"]["conflict"], 1)
        self.assertTrue(Customer.objects.filter(pk=customer_operation["payload"]["id"]).exists())
        self.assertFalse(Order.objects.exists())

    def test_invalid_batch_operation_gets_durable_rejected_receipt(self):
        operation = {
            "operation_id": str(uuid.uuid4()), "operation_type": "order_create",
            "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
            "client_version": 1, "payload": {"id": str(uuid.uuid4()), "items": []},
        }

        response = self.client.post(
            self.batch_url, {"device_id": str(self.device.id), "operations": [operation]}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["counts"]["rejected"], 1)
        receipt = SyncOperationReceipt.objects.get(operation_id=operation["operation_id"])
        self.assertEqual(receipt.status, SyncOperationReceipt.Status.REJECTED)
        self.assertEqual(receipt.conflict_code, "invalid_payload")
        self.assertFalse(hasattr(receipt, "payload"))

    def test_batch_retry_reuses_receipts_without_duplicate_entities(self):
        operation = {
            "operation_id": str(uuid.uuid4()), "operation_type": "customer_create",
            "idempotency_key": str(uuid.uuid4()), "client_timestamp": timezone.now().isoformat(),
            "client_version": 1,
            "payload": {"id": str(uuid.uuid4()), "full_name": "Customer", "email": "retry@example.test"},
        }
        batch = {"device_id": str(self.device.id), "operations": [operation]}

        first = self.client.post(self.batch_url, batch, format="json")
        second = self.client.post(self.batch_url, batch, format="json")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(SyncOperationReceipt.objects.count(), 1)
