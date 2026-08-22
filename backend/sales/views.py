import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from accounts.permissions import IsSeller

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer
from .services import IdempotencyConflictError, InvalidOrderReferenceError, create_order


class IdempotencyConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The idempotency key was already used for a different operation.")
    default_code = "idempotency_conflict"


class InvalidOrderReferenceApiError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _("The customer, device, or one of the products is unavailable.")
    default_code = "invalid_order_reference"


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Order.objects.filter(seller=self.request.user).prefetch_related("items")

    def get_serializer_class(self):
        return OrderCreateSerializer if self.request.method == "POST" else OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        supplied_key = request.headers.get("Idempotency-Key")
        try:
            idempotency_key = uuid.UUID(supplied_key) if supplied_key else None
        except ValueError as error:
            raise ValidationError({"idempotency_key": _("A valid UUID is required.")}) from error
        if idempotency_key is None:
            raise ValidationError({"idempotency_key": _("This header is required.")})

        try:
            result = create_order(
                actor=request.user,
                order_id=serializer.validated_data["id"],
                customer_id=serializer.validated_data["customer_id"],
                device_id=serializer.validated_data["device_id"],
                client_created_at=serializer.validated_data["client_created_at"],
                idempotency_key=idempotency_key,
                items=serializer.validated_data["items"],
                correlation_id=request.correlation_id,
            )
        except IdempotencyConflictError as error:
            raise IdempotencyConflictApiError from error
        except InvalidOrderReferenceError as error:
            raise InvalidOrderReferenceApiError from error

        output = OrderSerializer(result.order)
        response_status = status.HTTP_201_CREATED if result.created else status.HTTP_200_OK
        return Response(output.data, status=response_status)
