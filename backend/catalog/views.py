from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException

from accounts.permissions import IsSeller

from .models import Customer, Product
from .serializers import CustomerSerializer, ProductSerializer
from .services import DuplicateCustomerError, create_customer


class DuplicateCustomerApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("A customer with the supplied information already exists.")
    default_code = "duplicate_customer"


class CustomerListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeller]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(is_active=True)

    def perform_create(self, serializer):
        try:
            serializer.instance = create_customer(
                actor=self.request.user,
                full_name=serializer.validated_data["full_name"],
                email=serializer.validated_data.get("email"),
                phone=serializer.validated_data.get("phone"),
                identity_document=serializer.validated_data.get("identity_document"),
                correlation_id=self.request.correlation_id,
            )
        except DuplicateCustomerError as error:
            raise DuplicateCustomerApiError from error


class ProductListView(generics.ListAPIView):
    permission_classes = [IsSeller]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
