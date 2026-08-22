import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import Device, UserProfile
from catalog.models import Customer, Product
from fulfillment.models import Delivery, Invoice, InvoiceItem
from payments.models import CommissionMovement, PaymentConfirmation, PaymentReport
from sales.models import Order, OrderItem

from .models import CommissionSettlement
from .services import SettlementConflictError, confirm_settlement


class CommissionSettlementTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.seller = user_model.objects.create_user(username="seller", password="StrongPassword123!")
        self.admin_user = user_model.objects.create_user(username="admin", password="StrongPassword123!")
        UserProfile.objects.create(user=self.seller, role=UserProfile.Role.SELLER)
        UserProfile.objects.create(user=self.admin_user, role=UserProfile.Role.ADMIN)
        device = Device.objects.create(user=self.seller, platform=Device.Platform.ANDROID, app_version="1.0.0")
        customer = Customer.objects.create(full_name="Customer", email="customer@example.test", created_by=self.seller)
        product = Product.objects.create(
            sku="PRODUCT-1", name="Product", price=Decimal("100.00"), commission_amount=Decimal("30.00")
        )
        order = Order.objects.create(
            seller=self.seller, customer=customer, device=device, status=Order.Status.DELIVERED,
            total=Decimal("100.00"), idempotency_key=uuid.uuid4(), request_hash="a" * 64,
            client_created_at=timezone.now(),
        )
        order_item = OrderItem.objects.create(
            order=order, product=product, product_sku=product.sku, product_name=product.name,
            unit_price=product.price, unit_commission=product.commission_amount,
            quantity=1, line_total=Decimal("100.00"),
        )
        delivery = Delivery.objects.create(
            order=order, confirmed_by=self.admin_user, delivered_at=timezone.now(),
            idempotency_key=uuid.uuid4(), request_hash="b" * 64,
        )
        invoice = Invoice.objects.create(
            delivery=delivery, order=order, seller=self.seller, customer_id_snapshot=customer.id,
            customer_name=customer.full_name, total=order.total, status=Invoice.Status.PAID,
        )
        invoice_item = InvoiceItem.objects.create(
            invoice=invoice, order_item=order_item, product_id_snapshot=product.id,
            product_sku=product.sku, product_name=product.name, unit_price=product.price,
            unit_commission=product.commission_amount, quantity=1, line_total=Decimal("100.00"),
        )
        payment = PaymentReport.objects.create(
            invoice=invoice, seller=self.seller, device=device, method=PaymentReport.Method.CASH,
            amount=invoice.total, status=PaymentReport.Status.CONFIRMED,
            idempotency_key=uuid.uuid4(), request_hash="c" * 64, client_reported_at=timezone.now(),
        )
        confirmation = PaymentConfirmation.objects.create(
            payment_report=payment, confirmed_by=self.admin_user, confirmed_at=timezone.now(),
            idempotency_key=uuid.uuid4(), request_hash="d" * 64,
        )
        self.credit = CommissionMovement.objects.create(
            seller=self.seller, invoice=invoice, invoice_item=invoice_item,
            payment_confirmation=confirmation, movement_type=CommissionMovement.MovementType.CREDIT,
            amount=Decimal("30.00"), reference_type="payment_confirmation", reference_id=confirmation.id,
        )
        self.debit = CommissionMovement.objects.create(
            seller=self.seller, invoice=invoice, invoice_item=invoice_item,
            payment_confirmation=confirmation, movement_type=CommissionMovement.MovementType.DEBIT,
            amount=Decimal("10.00"), reference_type="return_confirmation", reference_id=uuid.uuid4(),
        )

    def settle(self, **overrides):
        values = {
            "actor": self.admin_user,
            "settlement_id": uuid.uuid4(),
            "seller_id": self.seller.id,
            "period_ends_at": timezone.now(),
            "confirmed_at": timezone.now(),
            "idempotency_key": uuid.uuid4(),
            "correlation_id": uuid.uuid4(),
        }
        values.update(overrides)
        return confirm_settlement(**values)

    def test_settlement_includes_all_available_credits_and_debits(self):
        result = self.settle()

        self.assertEqual(result.settlement.total, Decimal("20.00"))
        self.assertEqual(result.settlement.items.count(), 2)
        self.assertEqual(
            set(result.settlement.items.values_list("signed_amount", flat=True)),
            {Decimal("30.00"), Decimal("-10.00")},
        )
        self.assertFalse(CommissionMovement.objects.filter(status=CommissionMovement.Status.AVAILABLE).exists())

    def test_movements_cannot_be_settled_twice(self):
        self.settle()

        with self.assertRaises(SettlementConflictError):
            self.settle()

        self.assertEqual(CommissionSettlement.objects.count(), 1)

    def test_movements_after_period_end_remain_available(self):
        period_ends_at = timezone.now()
        CommissionMovement.objects.filter(pk=self.debit.pk).update(
            created_at=period_ends_at + timedelta(seconds=1)
        )

        result = self.settle(period_ends_at=period_ends_at, confirmed_at=period_ends_at)

        self.assertEqual(result.settlement.total, Decimal("30.00"))
        self.credit.refresh_from_db()
        self.debit.refresh_from_db()
        self.assertEqual(self.credit.status, CommissionMovement.Status.SETTLED)
        self.assertEqual(self.debit.status, CommissionMovement.Status.AVAILABLE)

    def test_non_positive_balance_is_rejected(self):
        self.credit.amount = Decimal("10.00")
        self.credit.save(update_fields=["amount"])

        with self.assertRaises(SettlementConflictError):
            self.settle()

        self.assertFalse(CommissionSettlement.objects.exists())
        self.assertEqual(CommissionMovement.objects.filter(status="available").count(), 2)

    def test_identical_retry_is_idempotent(self):
        key = uuid.uuid4()
        settlement_id = uuid.uuid4()
        period_ends_at = timezone.now()
        confirmed_at = timezone.now()
        first = self.settle(
            idempotency_key=key, settlement_id=settlement_id,
            period_ends_at=period_ends_at, confirmed_at=confirmed_at,
        )
        second = self.settle(
            idempotency_key=key, settlement_id=settlement_id,
            period_ends_at=period_ends_at, confirmed_at=confirmed_at,
        )

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(CommissionSettlement.objects.count(), 1)

    def test_seller_cannot_confirm_settlement_through_api(self):
        token = Token.objects.create(user=self.seller)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = client.post(
            "/api/commission-settlements/confirm/",
            {
                "id": str(uuid.uuid4()), "seller_id": self.seller.id,
                "period_ends_at": timezone.now().isoformat(), "confirmed_at": timezone.now().isoformat(),
            },
            format="json", HTTP_IDEMPOTENCY_KEY=str(uuid.uuid4()),
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(CommissionSettlement.objects.exists())

    def test_database_rejects_inconsistent_signed_amount(self):
        settlement = self.settle().settlement
        item = settlement.items.first()

        with self.assertRaises(IntegrityError), transaction.atomic():
            settlement.items.filter(pk=item.pk).update(signed_amount=Decimal("999.00"))

    def test_admin_action_settles_available_commissions(self):
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save(update_fields=["is_staff", "is_superuser"])
        client = APIClient()
        client.force_login(self.admin_user)

        response = client.post(
            "/admin/accounts/userprofile/",
            {
                "action": "settle_available_commissions",
                "_selected_action": str(self.seller.profile.pk),
                "index": "0",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(CommissionSettlement.objects.filter(seller=self.seller).exists())
        self.assertFalse(CommissionMovement.objects.filter(status="available").exists())
