import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from accounts.permissions import IsAdministrator, IsSeller

from .models import CommissionMovement, PaymentReport
from .serializers import (
    CommissionMovementSerializer,
    PaymentConfirmationCreateSerializer,
    PaymentConfirmationSerializer,
    PaymentReportCreateSerializer,
    PaymentReportSerializer,
)
from .services import (
    InvoiceNotPayableError,
    PaymentIdempotencyConflictError,
    PaymentNotConfirmableError,
    confirm_payment,
    report_payment,
)


class PaymentConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The payment operation conflicts with the current state or idempotency key.")
    default_code = "payment_conflict"


def parse_idempotency_key(request):
    supplied_key = request.headers.get("Idempotency-Key")
    try:
        key = uuid.UUID(supplied_key) if supplied_key else None
    except ValueError as error:
        raise ValidationError({"idempotency_key": _("A valid UUID is required.")}) from error
    if key is None:
        raise ValidationError({"idempotency_key": _("This header is required.")})
    return key


class PaymentReportListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeller]

    def get_queryset(self):
        return PaymentReport.objects.filter(seller=self.request.user)

    def get_serializer_class(self):
        return PaymentReportCreateSerializer if self.request.method == "POST" else PaymentReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = report_payment(
                actor=request.user,
                report_id=serializer.validated_data["id"],
                invoice_id=serializer.validated_data["invoice_id"],
                device_id=serializer.validated_data["device_id"],
                method=serializer.validated_data["method"],
                terminal_reference=serializer.validated_data["external_terminal_reference"],
                client_reported_at=serializer.validated_data["client_reported_at"],
                idempotency_key=parse_idempotency_key(request),
                correlation_id=request.correlation_id,
            )
        except (PaymentIdempotencyConflictError, InvoiceNotPayableError) as error:
            raise PaymentConflictApiError from error
        output = PaymentReportSerializer(result.instance)
        return Response(output.data, status=status.HTTP_201_CREATED if result.created else status.HTTP_200_OK)


class PaymentConfirmationCreateView(generics.GenericAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = PaymentConfirmationCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = confirm_payment(
                actor=request.user,
                confirmation_id=serializer.validated_data["id"],
                payment_report_id=serializer.validated_data["payment_report_id"],
                confirmed_at=serializer.validated_data["confirmed_at"],
                idempotency_key=parse_idempotency_key(request),
                correlation_id=request.correlation_id,
            )
        except (PaymentIdempotencyConflictError, PaymentNotConfirmableError) as error:
            raise PaymentConflictApiError from error
        output = PaymentConfirmationSerializer(result.instance)
        return Response(output.data, status=status.HTTP_201_CREATED if result.created else status.HTTP_200_OK)


class CommissionMovementListView(generics.ListAPIView):
    permission_classes = [IsSeller]
    serializer_class = CommissionMovementSerializer

    def get_queryset(self):
        return CommissionMovement.objects.filter(seller=self.request.user)
