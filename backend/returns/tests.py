import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Device, UserProfile
from catalog.models import Customer, Product
from fulfillment.models import Delivery, Invoice, InvoiceItem
from payments.models import CommissionMovement, PaymentConfirmation, PaymentReport
from sales.models import Order, OrderItem

from .models import ReturnConfirmation, ReturnReport
from .services import ReturnConflictError, confirm_return, report_return


class ReturnWorkflowTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.seller = user_model.objects.create_user(username="seller", password="StrongPassword123!")
        self.admin_user = user_model.objects.create_user(username="admin", password="StrongPassword123!")
        UserProfile.objects.create(user=self.seller, role=UserProfile.Role.SELLER)
        UserProfile.objects.create(user=self.admin_user, role=UserProfile.Role.ADMIN)
        self.device = Device.objects.create(
            user=self.seller, platform=Device.Platform.ANDROID, app_version="1.0.0"
        )
        customer = Customer.objects.create(
            full_name="Customer", email="customer@example.test", created_by=self.seller
        )
        product = Product.objects.create(
            sku="PRODUCT-1", name="Product", price=Decimal("100.00"),
            commission_amount=Decimal("7.50"),
        )
        order = Order.objects.create(
            seller=self.seller, customer=customer, device=self.device, status=Order.Status.DELIVERED,
            total=Decimal("300.00"), idempotency_key=uuid.uuid4(), request_hash="a" * 64,
            client_created_at=timezone.now(),
        )
        order_item = OrderItem.objects.create(
            order=order, product=product, product_sku=product.sku, product_name=product.name,
            unit_price=product.price, unit_commission=product.commission_amount,
            quantity=3, line_total=Decimal("300.00"),
        )
        delivery = Delivery.objects.create(
            order=order, confirmed_by=self.admin_user, delivered_at=timezone.now(),
            idempotency_key=uuid.uuid4(), request_hash="b" * 64,
        )
        self.invoice = Invoice.objects.create(
            delivery=delivery, order=order, seller=self.seller, customer_id_snapshot=customer.id,
            customer_name=customer.full_name, total=order.total, status=Invoice.Status.PAID,
        )
        self.invoice_item = InvoiceItem.objects.create(
            invoice=self.invoice, order_item=order_item, product_id_snapshot=product.id,
            product_sku=product.sku, product_name=product.name, unit_price=product.price,
            unit_commission=product.commission_amount, quantity=3, line_total=Decimal("300.00"),
        )
        payment = PaymentReport.objects.create(
            invoice=self.invoice, seller=self.seller, device=self.device, method=PaymentReport.Method.CASH,
            amount=self.invoice.total, status=PaymentReport.Status.CONFIRMED,
            idempotency_key=uuid.uuid4(), request_hash="c" * 64, client_reported_at=timezone.now(),
        )
        self.payment_confirmation = PaymentConfirmation.objects.create(
            payment_report=payment, confirmed_by=self.admin_user, confirmed_at=timezone.now(),
            idempotency_key=uuid.uuid4(), request_hash="d" * 64,
        )
        CommissionMovement.objects.create(
            seller=self.seller, invoice=self.invoice, invoice_item=self.invoice_item,
            payment_confirmation=self.payment_confirmation,
            movement_type=CommissionMovement.MovementType.CREDIT, amount=Decimal("22.50"),
            reference_type="payment_confirmation", reference_id=self.payment_confirmation.id,
        )

    def report(self, quantity=1, key=None, report_id=None):
        return report_return(
            actor=self.seller, report_id=report_id or uuid.uuid4(), invoice_id=self.invoice.id,
            device_id=self.device.id, client_reported_at=timezone.now(),
            items=[{"invoice_item_id": self.invoice_item.id, "quantity": quantity}],
            idempotency_key=key or uuid.uuid4(), correlation_id=uuid.uuid4(),
        )

    def test_return_uses_invoice_snapshots_and_server_totals(self):
        result = self.report(quantity=2)

        self.assertTrue(result.created)
        self.assertEqual(result.instance.total, Decimal("200.00"))
        self.assertEqual(result.instance.commission_total, Decimal("15.00"))
        item = result.instance.items.get()
        self.assertEqual(item.unit_price, Decimal("100.00"))
        self.assertEqual(item.unit_commission, Decimal("7.50"))

    def test_cumulative_return_quantity_cannot_exceed_invoice(self):
        self.report(quantity=2)

        with self.assertRaises(ReturnConflictError):
            self.report(quantity=2)

        self.assertEqual(ReturnReport.objects.count(), 1)

    def test_report_retry_is_idempotent(self):
        key = uuid.uuid4()
        report_id = uuid.uuid4()
        reported_at = timezone.now()
        arguments = {
            "actor": self.seller, "report_id": report_id, "invoice_id": self.invoice.id,
            "device_id": self.device.id, "client_reported_at": reported_at,
            "items": [{"invoice_item_id": self.invoice_item.id, "quantity": 1}],
            "idempotency_key": key, "correlation_id": uuid.uuid4(),
        }

        first = report_return(**arguments)
        arguments["correlation_id"] = uuid.uuid4()
        second = report_return(**arguments)

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(ReturnReport.objects.count(), 1)

    def test_confirmation_creates_compensating_commission_debit(self):
        report = self.report(quantity=2).instance

        result = confirm_return(
            actor=self.admin_user, confirmation_id=uuid.uuid4(), return_report_id=report.id,
            confirmed_at=timezone.now(), idempotency_key=uuid.uuid4(), correlation_id=uuid.uuid4(),
        )

        self.assertTrue(result.created)
        report.refresh_from_db()
        self.assertEqual(report.status, ReturnReport.Status.CONFIRMED)
        debit = CommissionMovement.objects.get(movement_type=CommissionMovement.MovementType.DEBIT)
        self.assertEqual(debit.amount, Decimal("15.00"))
        self.assertEqual(debit.reference_type, "return_confirmation")
        self.assertEqual(debit.reference_id, result.instance.id)
        self.assertEqual(CommissionMovement.objects.filter(movement_type="credit").count(), 1)

    def test_seller_cannot_confirm_return_through_api(self):
        report = self.report().instance
        token = Token.objects.create(user=self.seller)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = client.post(
            "/api/returns/confirm/",
            {"id": str(uuid.uuid4()), "return_report_id": str(report.id), "confirmed_at": timezone.now().isoformat()},
            format="json", HTTP_IDEMPOTENCY_KEY=str(uuid.uuid4()),
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(ReturnConfirmation.objects.exists())
