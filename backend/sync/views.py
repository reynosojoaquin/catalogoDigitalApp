from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Device
from accounts.permissions import IsSeller

from .models import SyncChange, SyncDeviceCursor, SyncOperationReceipt
from .serializers import (
    CursorAcknowledgementSerializer, SyncCursorSerializer,
    SyncBatchSerializer, SyncCustomerDataSerializer, SyncCustomerOperationSerializer,
    SyncOrderDataSerializer, SyncReceiptSerializer,
)
from .services import (
    SyncIdempotencyConflictError, record_rejected_operation, serialize_change,
    sync_customer_create, sync_order_create,
)


class SyncConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The idempotency key was used for a different synchronization operation.")


class SyncCustomerOperationView(generics.ListCreateAPIView):
    permission_classes = [IsSeller]

    def get_queryset(self):
        return SyncOperationReceipt.objects.filter(seller=self.request.user)

    def get_serializer_class(self):
        return SyncCustomerOperationSerializer if self.request.method == "POST" else SyncReceiptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        device = Device.objects.filter(
            pk=values["device_id"], user=request.user, is_active=True
        ).first()
        if not device:
            raise ValidationError({"device_id": _("An active device owned by the seller is required.")})
        customer = values["customer"]
        try:
            receipt, created = sync_customer_create(
                actor=request.user, device=device, operation_id=values["operation_id"],
                idempotency_key=values["idempotency_key"],
                client_timestamp=values["client_timestamp"], client_version=values["client_version"],
                customer_id=customer["id"], full_name=customer["full_name"],
                email=customer.get("email"), phone=customer.get("phone"),
                identity_document=customer.get("identity_document"),
                correlation_id=request.correlation_id,
            )
        except SyncIdempotencyConflictError as error:
            raise SyncConflictApiError from error
        output = SyncReceiptSerializer(receipt)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(output.data, status=response_status)


class CatalogChangeFeedView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        try:
            after = max(int(request.query_params.get("after", 0)), 0)
            limit = min(max(int(request.query_params.get("limit", 100)), 1), 200)
        except ValueError as error:
            raise ValidationError(_("Cursor and limit must be integers.")) from error
        changes = list(SyncChange.objects.filter(sequence__gt=after)[:limit])
        next_cursor = changes[-1].sequence if changes else after
        return Response({
            "changes": [serialize_change(change) for change in changes],
            "next_cursor": next_cursor,
            "has_more": SyncChange.objects.filter(sequence__gt=next_cursor).exists(),
        })


class CursorAcknowledgementView(generics.GenericAPIView):
    permission_classes = [IsSeller]
    serializer_class = CursorAcknowledgementSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = Device.objects.filter(
            pk=serializer.validated_data["device_id"], user=request.user, is_active=True
        ).first()
        if not device:
            raise ValidationError({"device_id": _("An active device owned by the seller is required.")})
        sequence = serializer.validated_data["sequence"]
        maximum = SyncChange.objects.order_by("-sequence").values_list("sequence", flat=True).first() or 0
        cursor, _cursor_created = SyncDeviceCursor.objects.select_for_update().get_or_create(device=device)
        if sequence < cursor.last_sequence or sequence > maximum:
            raise ValidationError({"sequence": _("The cursor cannot move backwards or beyond the server.")})
        cursor.last_sequence = sequence
        cursor.save(update_fields=["last_sequence", "acknowledged_at"])
        return Response(SyncCursorSerializer(cursor).data)


class SyncBatchView(generics.GenericAPIView):
    permission_classes = [IsSeller]
    serializer_class = SyncBatchSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = Device.objects.filter(
            pk=serializer.validated_data["device_id"], user=request.user, is_active=True
        ).first()
        if not device:
            raise ValidationError({"device_id": _("An active device owned by the seller is required.")})

        results = []
        for operation in serializer.validated_data["operations"]:
            results.append(self.process_operation(request, device, operation))
        counts = {
            receipt_status: sum(result["status"] == receipt_status for result in results)
            for receipt_status in SyncOperationReceipt.Status.values
        }
        return Response({"results": results, "counts": counts})

    def process_operation(self, request, device, operation):
        payload_serializer_class = (
            SyncCustomerDataSerializer
            if operation["operation_type"] == "customer_create"
            else SyncOrderDataSerializer
        )
        payload_serializer = payload_serializer_class(data=operation["payload"])
        if operation["client_version"] != 1 or not payload_serializer.is_valid():
            try:
                receipt, _created = record_rejected_operation(
                    actor=request.user, device=device, conflict_code="invalid_payload",
                    **operation,
                )
                return SyncReceiptSerializer(receipt).data
            except SyncIdempotencyConflictError:
                return self.idempotency_conflict_result(operation)

        values = payload_serializer.validated_data
        try:
            if operation["operation_type"] == "customer_create":
                receipt, _created = sync_customer_create(
                    actor=request.user, device=device,
                    operation_id=operation["operation_id"],
                    idempotency_key=operation["idempotency_key"],
                    client_timestamp=operation["client_timestamp"],
                    client_version=operation["client_version"],
                    customer_id=values["id"], full_name=values["full_name"],
                    email=values.get("email"), phone=values.get("phone"),
                    identity_document=values.get("identity_document"),
                    correlation_id=request.correlation_id,
                )
            else:
                receipt, _created = sync_order_create(
                    actor=request.user, device=device,
                    operation_id=operation["operation_id"],
                    idempotency_key=operation["idempotency_key"],
                    client_timestamp=operation["client_timestamp"],
                    client_version=operation["client_version"],
                    order_id=values["id"], customer_id=values["customer_id"],
                    client_created_at=values["client_created_at"], items=values["items"],
                    correlation_id=request.correlation_id,
                )
            return SyncReceiptSerializer(receipt).data
        except SyncIdempotencyConflictError:
            return self.idempotency_conflict_result(operation)

    @staticmethod
    def idempotency_conflict_result(operation):
        return {
            "operation_id": str(operation["operation_id"]),
            "entity_type": operation["operation_type"].removesuffix("_create"),
            "status": SyncOperationReceipt.Status.CONFLICT,
            "conflict_code": "idempotency_mismatch",
        }
