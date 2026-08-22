import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from accounts.permissions import IsAdministrator, IsSeller

from .models import Invoice
from .serializers import DeliveryConfirmationSerializer, DeliverySerializer, InvoiceSerializer
from .services import (
    DeliveryIdempotencyConflictError,
    OrderNotDeliverableError,
    confirm_complete_delivery,
)


class DeliveryIdempotencyConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The idempotency key was already used for a different delivery.")
    default_code = "idempotency_conflict"


class OrderNotDeliverableApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The order is not available for complete delivery.")
    default_code = "order_not_deliverable"


class DeliveryConfirmationView(generics.GenericAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = DeliveryConfirmationSerializer

    def post(self, request):
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
            result = confirm_complete_delivery(
                actor=request.user,
                delivery_id=serializer.validated_data["id"],
                order_id=serializer.validated_data["order_id"],
                delivered_at=serializer.validated_data["delivered_at"],
                idempotency_key=idempotency_key,
                correlation_id=request.correlation_id,
            )
        except DeliveryIdempotencyConflictError as error:
            raise DeliveryIdempotencyConflictApiError from error
        except OrderNotDeliverableError as error:
            raise OrderNotDeliverableApiError from error

        output = DeliverySerializer(result.delivery)
        response_status = status.HTTP_201_CREATED if result.created else status.HTTP_200_OK
        return Response(output.data, status=response_status)


class InvoiceListView(generics.ListAPIView):
    permission_classes = [IsSeller]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(seller=self.request.user).prefetch_related("items")
