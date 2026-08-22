import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from audit.models import AuditEvent

from .models import Customer, Product


class SellerApiTestCase(APITestCase):
    def create_user(self, username, role=UserProfile.Role.SELLER):
        user = get_user_model().objects.create_user(username=username, password="StrongPassword123!")
        UserProfile.objects.create(user=user, role=role)
        return user

    def authenticate(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


class CustomerApiTests(SellerApiTestCase):
    url = "/api/customers/"

    def setUp(self):
        self.seller = self.create_user("seller")
        self.authenticate(self.seller)

    def test_seller_creates_customer_without_storing_raw_identity_document(self):
        response = self.client.post(
            self.url,
            {
                "full_name": "  María   Pérez  ",
                "email": "MARIA@EXAMPLE.COM",
                "phone": "+1 (809) 555-0101",
                "identity_document": "001-1234567-8",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        customer = Customer.objects.get(pk=response.data["id"])
        self.assertEqual(customer.full_name, "María Pérez")
        self.assertEqual(customer.email, "maria@example.com")
        self.assertEqual(customer.phone, "+18095550101")
        self.assertNotEqual(customer.identity_document_hash, "001-1234567-8")
        self.assertNotIn("identity_document", response.data)
        self.assertTrue(
            AuditEvent.objects.filter(
                actor=self.seller,
                action="customer.created",
                resource_id=str(customer.id),
            ).exists()
        )

    def test_duplicate_email_is_rejected_case_insensitively(self):
        Customer.objects.create(
            full_name="Existing Customer",
            email="person@example.com",
            created_by=self.seller,
        )

        response = self.client.post(
            self.url,
            {"full_name": "Duplicate", "email": "PERSON@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(Customer.objects.count(), 1)

    def test_duplicate_identity_document_is_rejected_after_normalization(self):
        first = self.client.post(
            self.url,
            {"full_name": "First", "identity_document": "001-1234567-8"},
            format="json",
        )

        second = self.client.post(
            self.url,
            {"full_name": "Second", "identity_document": "00112345678"},
            format="json",
        )

        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_at_least_one_valid_identifier_is_required(self):
        response = self.client.post(
            self.url,
            {"full_name": "No Identifier", "phone": "---"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_seller_sees_all_active_customers_but_not_inactive_ones(self):
        other_seller = self.create_user("other-seller")
        visible = Customer.objects.create(
            full_name="Visible",
            email="visible@example.com",
            created_by=other_seller,
        )
        Customer.objects.create(
            full_name="Inactive",
            email="inactive@example.com",
            is_active=False,
            created_by=other_seller,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [str(visible.id)])

    def test_admin_role_cannot_use_seller_customer_api(self):
        admin_user = self.create_user("admin", UserProfile.Role.ADMIN)
        self.client.credentials()
        self.authenticate(admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)


class ProductApiTests(SellerApiTestCase):
    url = "/api/products/"

    def setUp(self):
        self.seller = self.create_user("seller")
        self.authenticate(self.seller)

    def test_seller_sees_only_active_products_with_decimal_values(self):
        visible = Product.objects.create(
            sku=" sku-1 ",
            name="Visible Product",
            price=Decimal("125.50"),
            commission_amount=Decimal("10.25"),
        )
        Product.objects.create(
            sku="SKU-2",
            name="Inactive Product",
            price=Decimal("50.00"),
            commission_amount=Decimal("5.00"),
            is_active=False,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(visible.id))
        self.assertEqual(response.data[0]["sku"], "SKU-1")
        self.assertEqual(response.data[0]["price"], "125.50")
        self.assertEqual(response.data[0]["commission_amount"], "10.25")

    def test_product_api_is_read_only(self):
        response = self.client.post(
            self.url,
            {
                "sku": str(uuid.uuid4()),
                "name": "Product",
                "price": "10.00",
                "commission_amount": "1.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 405)
