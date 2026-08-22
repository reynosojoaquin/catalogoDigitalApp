import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from accounts.permissions import IsAdministrator, IsSeller

from .models import ReturnReport
from .serializers import (
    ReturnConfirmationCreateSerializer, ReturnConfirmationSerializer,
    ReturnReportCreateSerializer, ReturnReportSerializer,
)
from .services import ReturnConflictError, confirm_return, report_return


class ReturnConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The return conflicts with the invoice, quantities, or idempotency key.")


def parse_idempotency_key(request):
    try:
        return uuid.UUID(request.headers.get("Idempotency-Key", ""))
    except ValueError as error:
        raise ValidationError({"idempotency_key": _("A valid UUID header is required.")}) from error


class ReturnReportListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSeller]

    def get_queryset(self):
        return ReturnReport.objects.filter(seller=self.request.user).prefetch_related("items")

    def get_serializer_class(self):
        return ReturnReportCreateSerializer if self.request.method == "POST" else ReturnReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = report_return(
                actor=request.user, idempotency_key=parse_idempotency_key(request),
                correlation_id=request.correlation_id, **serializer.validated_data,
            )
        except ReturnConflictError as error:
            raise ReturnConflictApiError from error
        output = ReturnReportSerializer(result.instance)
        return Response(output.data, status=status.HTTP_201_CREATED if result.created else status.HTTP_200_OK)


class ReturnConfirmationCreateView(generics.GenericAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = ReturnConfirmationCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = confirm_return(
                actor=request.user, idempotency_key=parse_idempotency_key(request),
                correlation_id=request.correlation_id, **serializer.validated_data,
            )
        except ReturnConflictError as error:
            raise ReturnConflictApiError from error
        output = ReturnConfirmationSerializer(result.instance)
        return Response(output.data, status=status.HTTP_201_CREATED if result.created else status.HTTP_200_OK)
