import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import Device, UserProfile
from audit.models import AuditEvent
from catalog.models import Customer, Product
from fulfillment.models import Delivery, Invoice, InvoiceItem
from sales.models import Order, OrderItem

from .models import CommissionMovement, PaymentConfirmation, PaymentReport


class PaymentApiTests(APITestCase):
    payment_url = "/api/payments/"
    confirmation_url = "/api/payments/confirm/"
    commission_url = "/api/commissions/"

    def setUp(self):
        self.seller = self.create_user("seller", UserProfile.Role.SELLER)
        self.admin_user = self.create_user("admin", UserProfile.Role.ADMIN)
        self.device = Device.objects.create(
            user=self.seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )
        customer = Customer.objects.create(
            full_name="Customer",
            email="customer@example.test",
            created_by=self.seller,
        )
        product = Product.objects.create(
            sku="PRODUCT-1",
            name="Product",
            price=Decimal("125.50"),
            commission_amount=Decimal("10.25"),
        )
        order = Order.objects.create(
            seller=self.seller,
            customer=customer,
            device=self.device,
            status=Order.Status.DELIVERED,
            total=Decimal("251.00"),
            idempotency_key=uuid.uuid4(),
            request_hash="a" * 64,
            client_created_at=timezone.now(),
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_sku=product.sku,
            product_name=product.name,
            unit_price=product.price,
            unit_commission=product.commission_amount,
            quantity=2,
            line_total=Decimal("251.00"),
        )
        delivery = Delivery.objects.create(
            order=order,
            confirmed_by=self.admin_user,
            delivered_at=timezone.now(),
            idempotency_key=uuid.uuid4(),
            request_hash="b" * 64,
        )
        self.invoice = Invoice.objects.create(
            delivery=delivery,
            order=order,
            seller=self.seller,
            customer_id_snapshot=customer.id,
            customer_name=customer.full_name,
            customer_email=customer.email,
            total=order.total,
        )
        self.invoice_item = InvoiceItem.objects.create(
            invoice=self.invoice,
            order_item=order_item,
            product_id_snapshot=product.id,
            product_sku=product.sku,
            product_name=product.name,
            unit_price=product.price,
            unit_commission=product.commission_amount,
            quantity=2,
            line_total=Decimal("251.00"),
        )

    def create_user(self, username, role):
        user = get_user_model().objects.create_user(username=username, password="StrongPassword123!")
        UserProfile.objects.create(user=user, role=role)
        return user

    def authenticate(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def payment_payload(self, **overrides):
        payload = {
            "id": str(uuid.uuid4()),
            "invoice_id": str(self.invoice.id),
            "device_id": str(self.device.id),
            "method": PaymentReport.Method.CASH,
            "client_reported_at": timezone.now().isoformat(),
        }
        payload.update(overrides)
        return payload

    def post_payment(self, payload=None, idempotency_key=None):
        return self.client.post(
            self.payment_url,
            payload or self.payment_payload(),
            format="json",
            HTTP_IDEMPOTENCY_KEY=str(idempotency_key or uuid.uuid4()),
        )

    def confirmation_payload(self, report_id):
        return {
            "id": str(uuid.uuid4()),
            "payment_report_id": str(report_id),
            "confirmed_at": timezone.now().isoformat(),
        }

    def post_confirmation(self, payload, idempotency_key=None):
        return self.client.post(
            self.confirmation_url,
            payload,
            format="json",
            HTTP_IDEMPOTENCY_KEY=str(idempotency_key or uuid.uuid4()),
        )

    def test_seller_reports_cash_payment_for_server_invoice_total(self):
        self.authenticate(self.seller)
        payload = self.payment_payload(amount="0.01")

        response = self.post_payment(payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["amount"], "251.00")
        self.assertEqual(response.data["status"], PaymentReport.Status.REPORTED)
        self.assertTrue(AuditEvent.objects.filter(action="payment.reported").exists())

    def test_card_terminal_requires_external_reference(self):
        self.authenticate(self.seller)

        response = self.post_payment(self.payment_payload(method=PaymentReport.Method.EXTERNAL_CARD_TERMINAL))

        self.assertEqual(response.status_code, 400)

    def test_cash_rejects_terminal_reference(self):
        self.authenticate(self.seller)

        response = self.post_payment(self.payment_payload(external_terminal_reference="TERMINAL-REFERENCE"))

        self.assertEqual(response.status_code, 400)

    def test_card_number_cannot_be_used_as_terminal_reference(self):
        self.authenticate(self.seller)
        payload = self.payment_payload(
            method=PaymentReport.Method.EXTERNAL_CARD_TERMINAL,
            external_terminal_reference="4111 1111 1111 1111",
        )

        response = self.post_payment(payload)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(PaymentReport.objects.exists())

    def test_payment_report_is_idempotent(self):
        self.authenticate(self.seller)
        payload = self.payment_payload()
        key = uuid.uuid4()

        first = self.post_payment(payload, key)
        second = self.post_payment(payload, key)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(PaymentReport.objects.count(), 1)

    def test_seller_cannot_report_payment_for_another_seller_invoice(self):
        other_seller = self.create_user("other-seller", UserProfile.Role.SELLER)
        other_device = Device.objects.create(
            user=other_seller,
            platform=Device.Platform.ANDROID,
            app_version="1.0.0",
        )
        self.authenticate(other_seller)

        response = self.post_payment(self.payment_payload(device_id=str(other_device.id)))

        self.assertEqual(response.status_code, 409)

    def test_administrator_confirmation_pays_invoice_and_credits_fixed_commission(self):
        self.authenticate(self.seller)
        report_response = self.post_payment()
        self.client.credentials()
        self.authenticate(self.admin_user)

        response = self.post_confirmation(self.confirmation_payload(report_response.data["id"]))

        self.assertEqual(response.status_code, 201)
        self.invoice.refresh_from_db()
        report = PaymentReport.objects.get(pk=report_response.data["id"])
        movement = CommissionMovement.objects.get(invoice=self.invoice)
        self.assertEqual(self.invoice.status, Invoice.Status.PAID)
        self.assertEqual(report.status, PaymentReport.Status.CONFIRMED)
        self.assertEqual(movement.amount, Decimal("20.50"))
        self.assertEqual(movement.seller, self.seller)
        self.assertEqual(movement.status, CommissionMovement.Status.AVAILABLE)
        self.assertTrue(AuditEvent.objects.filter(action="payment.confirmed").exists())
        self.assertTrue(AuditEvent.objects.filter(action="commission.credited").exists())

    def test_seller_cannot_confirm_payment(self):
        self.authenticate(self.seller)
        report = self.post_payment()

        response = self.post_confirmation(self.confirmation_payload(report.data["id"]))

        self.assertEqual(response.status_code, 403)
        self.assertFalse(PaymentConfirmation.objects.exists())

    def test_confirmation_retry_does_not_duplicate_commission(self):
        self.authenticate(self.seller)
        report = self.post_payment()
        self.client.credentials()
        self.authenticate(self.admin_user)
        payload = self.confirmation_payload(report.data["id"])
        key = uuid.uuid4()

        first = self.post_confirmation(payload, key)
        second = self.post_confirmation(payload, key)

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(PaymentConfirmation.objects.count(), 1)
        self.assertEqual(CommissionMovement.objects.count(), 1)

    def test_seller_lists_only_own_commissions(self):
        self.authenticate(self.seller)
        report = self.post_payment()
        self.client.credentials()
        self.authenticate(self.admin_user)
        self.post_confirmation(self.confirmation_payload(report.data["id"]))
        self.client.credentials()
        self.authenticate(self.seller)

        response = self.client.get(self.commission_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["amount"], "20.50")
