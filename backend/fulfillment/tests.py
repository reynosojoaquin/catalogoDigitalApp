import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import Device, UserProfile
from audit.models import AuditEvent
from catalog.models import Customer, Product
from sales.models import Order, OrderItem

from .models import Delivery, Invoice


class FulfillmentApiTests(APITestCase):
    delivery_url = "/api/deliveries/complete/"
    invoice_url = "/api/invoices/"

    def setUp(self):
        self.seller = self.create_user("seller", UserProfile.Role.SELLER)
        self.admin_user = self.create_user("admin", UserProfile.Role.ADMIN)
        self.device = Device.objects.create(
            user=self.seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )
        self.customer = Customer.objects.create(
            full_name="Customer",
            email="customer@example.test",
            phone="+18095550101",
            created_by=self.seller,
        )
        self.product = Product.objects.create(
            sku="PRODUCT-1",
            name="Product",
            price=Decimal("125.50"),
            commission_amount=Decimal("10.25"),
        )
        self.order = Order.objects.create(
            seller=self.seller,
            customer=self.customer,
            device=self.device,
            total=Decimal("251.00"),
            idempotency_key=uuid.uuid4(),
            request_hash="a" * 64,
            client_created_at=timezone.now(),
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_sku=self.product.sku,
            product_name=self.product.name,
            unit_price=self.product.price,
            unit_commission=self.product.commission_amount,
            quantity=2,
            line_total=Decimal("251.00"),
        )

    def create_user(self, username, role):
        user = get_user_model().objects.create_user(username=username, password="StrongPassword123!")
        UserProfile.objects.create(user=user, role=role)
        return user

    def authenticate(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def payload(self, **overrides):
        payload = {
            "id": str(uuid.uuid4()),
            "order_id": str(self.order.id),
            "delivered_at": timezone.now().isoformat(),
        }
        payload.update(overrides)
        return payload

    def confirm_delivery(self, payload=None, idempotency_key=None):
        return self.client.post(
            self.delivery_url,
            payload or self.payload(),
            format="json",
            HTTP_IDEMPOTENCY_KEY=str(idempotency_key or uuid.uuid4()),
        )

    def test_administrator_confirms_complete_delivery_and_invoice_is_generated(self):
        self.authenticate(self.admin_user)

        response = self.confirm_delivery()

        self.assertEqual(response.status_code, 201)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.DELIVERED)
        self.assertEqual(self.order.version, 2)
        invoice = Invoice.objects.get(order=self.order)
        self.assertEqual(invoice.total, Decimal("251.00"))
        self.assertEqual(invoice.status, Invoice.Status.UNPAID)
        self.assertEqual(invoice.items.count(), self.order.items.count())
        item = invoice.items.get()
        self.assertEqual(item.unit_price, Decimal("125.50"))
        self.assertEqual(item.unit_commission, Decimal("10.25"))
        self.assertTrue(
            AuditEvent.objects.filter(action="delivery.completed", resource_id=response.data["id"]).exists()
        )
        self.assertTrue(
            AuditEvent.objects.filter(action="invoice.issued", resource_id=str(invoice.id)).exists()
        )

    def test_seller_cannot_confirm_delivery(self):
        self.authenticate(self.seller)

        response = self.confirm_delivery()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Delivery.objects.exists())
        self.assertFalse(Invoice.objects.exists())

    def test_identical_retry_returns_same_delivery_and_invoice(self):
        self.authenticate(self.admin_user)
        payload = self.payload()
        idempotency_key = uuid.uuid4()

        first = self.confirm_delivery(payload, idempotency_key)
        second = self.confirm_delivery(payload, idempotency_key)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.data["id"], second.data["id"])
        self.assertEqual(first.data["invoice"]["id"], second.data["invoice"]["id"])
        self.assertEqual(Delivery.objects.count(), 1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertTrue(
            AuditEvent.objects.filter(
                action="delivery.idempotent_replay",
                resource_id=first.data["id"],
            ).exists()
        )

    def test_same_key_with_changed_delivery_is_rejected(self):
        self.authenticate(self.admin_user)
        payload = self.payload()
        idempotency_key = uuid.uuid4()
        self.confirm_delivery(payload, idempotency_key)
        changed = {**payload, "id": str(uuid.uuid4())}

        response = self.confirm_delivery(changed, idempotency_key)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_order_cannot_be_delivered_twice_with_different_keys(self):
        self.authenticate(self.admin_user)
        self.confirm_delivery()

        response = self.confirm_delivery()

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Invoice.objects.count(), 1)

    def test_invoice_snapshots_survive_customer_and_product_changes(self):
        self.authenticate(self.admin_user)
        self.confirm_delivery()
        invoice = Invoice.objects.get(order=self.order)
        self.customer.full_name = "Changed Customer"
        self.customer.email = "changed@example.test"
        self.customer.save()
        self.product.name = "Changed Product"
        self.product.price = Decimal("999.99")
        self.product.save()

        invoice.refresh_from_db()
        item = invoice.items.get()

        self.assertEqual(invoice.customer_name, "Customer")
        self.assertEqual(invoice.customer_email, "customer@example.test")
        self.assertEqual(item.product_name, "Product")
        self.assertEqual(item.unit_price, Decimal("125.50"))

    def test_seller_only_lists_own_invoices(self):
        self.authenticate(self.admin_user)
        self.confirm_delivery()
        self.client.credentials()
        self.authenticate(self.seller)

        response = self.client.get(self.invoice_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["order_id"], str(self.order.id))

    def test_invoice_does_not_exist_before_delivery(self):
        self.authenticate(self.seller)

        response = self.client.get(self.invoice_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_admin_action_confirms_delivery_through_domain_service(self):
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save(update_fields=["is_staff", "is_superuser"])
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/admin/sales/order/",
            {"action": "confirm_deliveries", "_selected_action": str(self.order.id), "index": "0"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Delivery.objects.filter(order=self.order, confirmed_by=self.admin_user).exists())
        self.assertTrue(Invoice.objects.filter(order=self.order).exists())
        self.assertTrue(AuditEvent.objects.filter(action="delivery.completed").exists())

    def test_seller_role_cannot_invoke_admin_delivery_action(self):
        self.seller.is_staff = True
        self.seller.user_permissions.add(
            Permission.objects.get(codename="view_order"),
            Permission.objects.get(codename="change_order"),
        )
        self.seller.save(update_fields=["is_staff"])
        self.client.force_login(self.seller)

        response = self.client.post(
            "/admin/sales/order/",
            {"action": "confirm_deliveries", "_selected_action": str(self.order.id), "index": "0"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Delivery.objects.exists())
