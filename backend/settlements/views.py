import uuid

from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from accounts.permissions import IsAdministrator, IsSeller

from .models import CommissionSettlement
from .serializers import SettlementConfirmationSerializer, SettlementSerializer
from .services import SettlementConflictError, confirm_settlement


class SettlementConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("No positive commission balance is available for this settlement.")


def parse_idempotency_key(request):
    try:
        return uuid.UUID(request.headers.get("Idempotency-Key", ""))
    except ValueError as error:
        raise ValidationError({"idempotency_key": _("A valid UUID header is required.")}) from error


class SettlementConfirmationView(generics.GenericAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = SettlementConfirmationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = confirm_settlement(
                actor=request.user,
                idempotency_key=parse_idempotency_key(request),
                correlation_id=request.correlation_id,
                **serializer.validated_data,
            )
        except SettlementConflictError as error:
            raise SettlementConflictApiError from error
        output = SettlementSerializer(result.settlement)
        return Response(output.data, status=status.HTTP_201_CREATED if result.created else status.HTTP_200_OK)


class SettlementListView(generics.ListAPIView):
    permission_classes = [IsSeller]
    serializer_class = SettlementSerializer

    def get_queryset(self):
        return CommissionSettlement.objects.filter(seller=self.request.user).prefetch_related("items")
