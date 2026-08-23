from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from payments.serializers import PaymentReportCreateSerializer
from returns.serializers import ReturnReportCreateSerializer

from accounts.models import Device
from accounts.permissions import IsSeller
from audit.models import AuditEvent

from .models import SyncChange, SyncDeviceCursor, SyncOperationReceipt
from .serializers import (
    CursorAcknowledgementSerializer, SyncCursorSerializer,
    SyncBatchSerializer, SyncCustomerDataSerializer, SyncCustomerOperationSerializer,
    SyncOrderDataSerializer, SyncReceiptSerializer,
)
from .services import (
    SyncIdempotencyConflictError, record_rejected_operation, serialize_business_change, serialize_change,
    sync_customer_create, sync_order_create, sync_payment_create, sync_return_create,
)


class SyncConflictApiError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("The idempotency key was used for a different synchronization operation.")


def audit_sync_conflict(request, operation_id, entity_type, conflict_code):
    AuditEvent.objects.create(
        actor=request.user,
        action="sync.operation_denied",
        resource_type=entity_type,
        resource_id=str(operation_id),
        result=AuditEvent.Result.DENIED,
        source="android",
        correlation_id=request.correlation_id,
        metadata={"status": SyncOperationReceipt.Status.CONFLICT, "conflict_code": conflict_code},
    )


def require_active_feed_device(request):
    device_id = request.query_params.get("device_id")
    if not device_id:
        raise ValidationError({"device_id": _("A device identifier is required.")})
    try:
        device = Device.objects.filter(pk=device_id, user=request.user, is_active=True).first()
    except (DjangoValidationError, ValueError, TypeError) as error:
        raise ValidationError({"device_id": _("A valid device identifier is required.")}) from error
    if not device:
        raise PermissionDenied(_("An active device owned by the seller is required."))
    return device


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
            audit_sync_conflict(
                request,
                values["operation_id"],
                "customer",
                "idempotency_mismatch",
            )
            raise SyncConflictApiError from error
        output = SyncReceiptSerializer(receipt)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(output.data, status=response_status)


class CatalogChangeFeedView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        require_active_feed_device(request)
        try:
            after = max(int(request.query_params.get("after", 0)), 0)
            limit = min(max(int(request.query_params.get("limit", 100)), 1), 200)
        except ValueError as error:
            raise ValidationError(_("Cursor and limit must be integers.")) from error
        changes = list(SyncChange.objects.filter(
            sequence__gt=after, entity_type__in=("customer", "product")
        )[:limit])
        next_cursor = changes[-1].sequence if changes else after
        return Response({
            "changes": [serialize_change(change) for change in changes],
            "next_cursor": next_cursor,
            "has_more": SyncChange.objects.filter(
                sequence__gt=next_cursor, entity_type__in=("customer", "product")
            ).exists(),
        })


class BusinessChangeFeedView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        require_active_feed_device(request)
        try:
            after = max(int(request.query_params.get("after", 0)), 0)
            limit = min(max(int(request.query_params.get("limit", 100)), 1), 200)
        except ValueError as error:
            raise ValidationError(_("Cursor and limit must be integers.")) from error
        changes = list(SyncChange.objects.filter(
            sequence__gt=after, seller=request.user
        )[:limit])
        next_cursor = changes[-1].sequence if changes else after
        return Response({
            "changes": [serialize_business_change(change) for change in changes],
            "next_cursor": next_cursor,
            "has_more": SyncChange.objects.filter(
                sequence__gt=next_cursor, seller=request.user
            ).exists(),
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
        payload_serializer_classes = {
            "customer_create": SyncCustomerDataSerializer,
            "order_create": SyncOrderDataSerializer,
            "payment_create": PaymentReportCreateSerializer,
            "return_create": ReturnReportCreateSerializer,
        }
        payload = operation["payload"]
        if not isinstance(payload, dict):
            try:
                receipt, _created = record_rejected_operation(
                    actor=request.user, device=device, conflict_code="invalid_payload",
                    **operation,
                )
                return SyncReceiptSerializer(receipt).data
            except SyncIdempotencyConflictError:
                return self.idempotency_conflict_result(request, operation)
        if operation["operation_type"] in ("payment_create", "return_create"):
            payload = {**payload, "device_id": str(device.id)}
        payload_serializer = payload_serializer_classes[operation["operation_type"]](data=payload)
        if operation["client_version"] != 1 or not payload_serializer.is_valid():
            try:
                receipt, _created = record_rejected_operation(
                    actor=request.user, device=device, conflict_code="invalid_payload",
                    **operation,
                )
                return SyncReceiptSerializer(receipt).data
            except SyncIdempotencyConflictError:
                return self.idempotency_conflict_result(request, operation)

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
            elif operation["operation_type"] == "order_create":
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
            elif operation["operation_type"] == "payment_create":
                receipt, _created = sync_payment_create(
                    actor=request.user, device=device,
                    operation_id=operation["operation_id"],
                    idempotency_key=operation["idempotency_key"],
                    client_timestamp=operation["client_timestamp"],
                    client_version=operation["client_version"],
                    report_id=values["id"], invoice_id=values["invoice_id"],
                    method=values["method"],
                    terminal_reference=values["external_terminal_reference"],
                    client_reported_at=values["client_reported_at"],
                    correlation_id=request.correlation_id,
                )
            else:
                receipt, _created = sync_return_create(
                    actor=request.user, device=device,
                    operation_id=operation["operation_id"],
                    idempotency_key=operation["idempotency_key"],
                    client_timestamp=operation["client_timestamp"],
                    client_version=operation["client_version"],
                    report_id=values["id"], invoice_id=values["invoice_id"],
                    client_reported_at=values["client_reported_at"], items=values["items"],
                    correlation_id=request.correlation_id,
                )
            return SyncReceiptSerializer(receipt).data
        except SyncIdempotencyConflictError:
            return self.idempotency_conflict_result(request, operation)

    @staticmethod
    def idempotency_conflict_result(request, operation):
        audit_sync_conflict(
            request,
            operation["operation_id"],
            operation["operation_type"].removesuffix("_create"),
            "idempotency_mismatch",
        )
        return {
            "operation_id": str(operation["operation_id"]),
            "entity_type": operation["operation_type"].removesuffix("_create"),
            "status": SyncOperationReceipt.Status.CONFLICT,
            "conflict_code": "idempotency_mismatch",
        }
