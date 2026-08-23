from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
import uuid

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Device, UserProfile
from audit.models import AuditEvent
from catalog.models import Customer, Product
from fulfillment.models import Invoice
from payments.models import CommissionMovement, PaymentReport
from returns.models import ReturnReport
from sales.models import Order
from fulfillment.services import DeliveryIdempotencyConflictError, OrderNotDeliverableError, confirm_complete_delivery
from payments.services import PaymentIdempotencyConflictError, PaymentNotConfirmableError, confirm_payment
from returns.services import ReturnConflictError, confirm_return
from settlements.services import SettlementConflictError, confirm_settlement


def _is_administrator(user):
    return user.is_active and (
        user.is_superuser
        or UserProfile.objects.filter(user=user, role=UserProfile.Role.ADMIN).exists()
    )


@login_required(login_url="/admin/login/")
def dashboard(request):
    if not _is_administrator(request.user):
        raise PermissionDenied

    context = {
        "page_title": _("Administration dashboard"),
        "metrics": [
            {"label": _("Active products"), "value": Product.objects.filter(is_active=True).count(), "url": "/app/catalog/"},
            {"label": _("Active customers"), "value": Customer.objects.filter(is_active=True).count(), "url": "/app/customers/"},
            {"label": _("Submitted orders"), "value": Order.objects.filter(status=Order.Status.SUBMITTED).count(), "url": "/app/orders/?status=submitted"},
            {"label": _("Unpaid invoices"), "value": Invoice.objects.filter(status=Invoice.Status.UNPAID).count(), "url": "/app/invoices/?status=unpaid"},
            {"label": _("Reported payments"), "value": PaymentReport.objects.filter(status=PaymentReport.Status.REPORTED).count(), "url": "/app/payments/?status=reported"},
            {"label": _("Reported returns"), "value": ReturnReport.objects.filter(status=ReturnReport.Status.REPORTED).count(), "url": "/app/returns/?status=reported"},
        ],
        "available_commissions": CommissionMovement.objects.filter(
            status=CommissionMovement.Status.AVAILABLE,
            movement_type=CommissionMovement.MovementType.CREDIT,
        ).aggregate(total=Sum("amount"))["total"],
        "active_devices": Device.objects.filter(is_active=True).count(),
        "recent_events": AuditEvent.objects.select_related("actor").order_by("-occurred_at")[:8],
    }
    return render(request, "dashboard/dashboard.html", context)


RESOURCE_CONFIG = {
    "users": {
        "title": _("Users"), "model": get_user_model(),
        "search": ("username", "email"),
        "columns": (("username", _("Username")), ("email", _("Email")), ("is_staff", _("Staff")), ("is_active", _("Status")), ("date_joined", _("Joined"))),
    },
    "catalog": {
        "title": _("Catalog"), "model": Product,
        "search": ("sku", "name"),
        "columns": (("sku", _("SKU")), ("name", _("Name")), ("price", _("Price")), ("commission_amount", _("Commission")), ("is_active", _("Status"))),
    },
    "customers": {
        "title": _("Customers"), "model": Customer,
        "search": ("full_name", "email", "phone"),
        "columns": (("full_name", _("Name")), ("email", _("Email")), ("phone", _("Phone")), ("is_active", _("Status")), ("created_at", _("Created"))),
    },
    "orders": {
        "title": _("Orders"), "model": Order,
        "search": ("id", "seller__username", "customer__full_name"),
        "columns": (("id", _("Order")), ("seller__username", _("Seller")), ("customer__full_name", _("Customer")), ("status", _("Status")), ("total", _("Total")), ("created_at", _("Created"))),
    },
    "invoices": {
        "title": _("Invoices"), "model": Invoice,
        "search": ("id", "seller__username", "customer_name"),
        "columns": (("id", _("Invoice")), ("customer_name", _("Customer")), ("seller__username", _("Seller")), ("status", _("Status")), ("total", _("Total")), ("issued_at", _("Issued"))),
    },
    "payments": {
        "title": _("Payments"), "model": PaymentReport,
        "search": ("id", "invoice__id", "seller__username"),
        "columns": (("id", _("Payment")), ("invoice__id", _("Invoice")), ("seller__username", _("Seller")), ("method", _("Method")), ("status", _("Status")), ("amount", _("Amount"))),
    },
    "returns": {
        "title": _("Returns"), "model": ReturnReport,
        "search": ("id", "invoice__id", "seller__username"),
        "columns": (("id", _("Return")), ("invoice__id", _("Invoice")), ("seller__username", _("Seller")), ("status", _("Status")), ("total", _("Total")), ("created_at", _("Created"))),
    },
    "commissions": {
        "title": _("Commissions"), "model": CommissionMovement,
        "search": ("id", "seller__username", "invoice__id"),
        "columns": (("id", _("Movement")), ("seller__username", _("Seller")), ("invoice__id", _("Invoice")), ("movement_type", _("Type")), ("status", _("Status")), ("amount", _("Amount")), ("created_at", _("Created"))),
    },
    "audit": {
        "title": _("Audit log"), "model": AuditEvent,
        "search": ("action", "resource_type", "resource_id", "actor__username"),
        "columns": (("occurred_at", _("Date")), ("action", _("Action")), ("actor__username", _("Actor")), ("resource_type", _("Resource")), ("result", _("Result"))),
    },
    "sellers": {
        "title": _("Sellers"), "model": UserProfile,
        "search": ("user__username",),
        "columns": (("user__username", _("Username")), ("role", _("Role")), ("user__is_active", _("Status")), ("created_at", _("Created"))),
    },
    "devices": {
        "title": _("Devices"), "model": Device,
        "search": ("id", "user__username", "app_version"),
        "columns": (("id", _("Device")), ("user__username", _("Seller")), ("platform", _("Platform")), ("app_version", _("App version")), ("is_active", _("Status")), ("last_seen_at", _("Last seen"))),
    },
}


def _value_for_column(obj, path):
    value = obj
    for part in path.split("__"):
        value = getattr(value, part, "")
        if value is None:
            return ""
    if isinstance(value, bool):
        return _("Active") if value else _("Inactive")
    if hasattr(value, "isoformat") and not isinstance(value, str):
        return value.strftime("%Y-%m-%d %H:%M")
    return value


@login_required(login_url="/admin/login/")
def resource_list(request, resource):
    if not _is_administrator(request.user):
        raise PermissionDenied
    config = RESOURCE_CONFIG.get(resource)
    if config is None:
        raise PermissionDenied
    queryset = config["model"].objects.all()
    for relation in {"seller", "customer", "invoice", "actor"}:
        if any(field.startswith(f"{relation}__") for field in config["search"]):
            queryset = queryset.select_related(relation)
    query = request.GET.get("q", "").strip()
    if query:
        search_query = Q()
        for field in config["search"]:
            search_query |= Q(**{f"{field}__icontains": query})
        queryset = queryset.filter(search_query)
    status_filter = request.GET.get("status", "").strip()
    if status_filter and "status" in [column[0] for column in config["columns"]]:
        queryset = queryset.filter(status=status_filter)
    paginator = Paginator(queryset, 25)
    page = paginator.get_page(request.GET.get("page"))
    rows = [{"url": f"/app/{resource}/{item.pk}/", "values": [_value_for_column(item, field) for field, _ in config["columns"]]} for item in page]
    statuses = []
    if hasattr(config["model"], "Status"):
        statuses = [(choice.value, choice.label) for choice in config["model"].Status]
    return render(request, "dashboard/resource_list.html", {
        "page_title": config["title"], "columns": [label for _, label in config["columns"]],
        "rows": rows, "page_obj": page, "query": query, "statuses": statuses,
        "status_filter": status_filter, "resource": resource,
    })


@login_required(login_url="/admin/login/")
def resource_detail(request, resource, pk):
    if not _is_administrator(request.user):
        raise PermissionDenied
    config = RESOURCE_CONFIG.get(resource)
    if config is None:
        raise PermissionDenied
    queryset = config["model"].objects.all()
    for relation in {"seller", "customer", "invoice", "actor"}:
        if any(field.startswith(f"{relation}__") for field, _ in config["columns"]):
            queryset = queryset.select_related(relation)
    item = get_object_or_404(queryset, pk=pk)
    fields = [{"label": label, "value": _value_for_column(item, field)} for field, label in config["columns"]]
    related = None
    if resource == "orders":
        related = {"title": _("Order items"), "columns": (_("Product"), _("Quantity"), _("Unit price"), _("Line total")), "rows": [[row.product_name, row.quantity, row.unit_price, row.line_total] for row in item.items.all()]}
    elif resource == "invoices":
        related = {"title": _("Invoice items"), "columns": (_("Product"), _("Quantity"), _("Unit price"), _("Line total")), "rows": [[row.product_name, row.quantity, row.unit_price, row.line_total] for row in item.items.all()]}
    elif resource == "returns":
        related = {"title": _("Returned items"), "columns": (_("Product"), _("Quantity"), _("Unit price"), _("Line total")), "rows": [[row.invoice_item.product_name, row.quantity, row.unit_price, row.line_total] for row in item.items.select_related("invoice_item").all()]}
    action = None
    if resource == "orders" and item.status == Order.Status.SUBMITTED:
        action = {"label": _("Confirm complete delivery"), "key": "delivery"}
    elif resource == "payments" and item.status == PaymentReport.Status.REPORTED:
        action = {"label": _("Confirm total payment"), "key": "payment"}
    elif resource == "returns" and item.status == ReturnReport.Status.REPORTED:
        action = {"label": _("Confirm return"), "key": "return"}
    elif resource == "commissions" and item.status == CommissionMovement.Status.AVAILABLE:
        action = {"label": _("Settle available commissions for this seller"), "key": "settlement"}
    elif resource == "devices" and item.is_active:
        action = {"label": _("Revoke device"), "key": "revoke_device"}
    elif resource == "users" and item != request.user:
        action = {"label": _("Deactivate user") if item.is_active else _("Activate user"), "key": "toggle_user", "desired_active": not item.is_active}
    return render(request, "dashboard/resource_detail.html", {
        "page_title": config["title"], "resource": resource, "item": item, "fields": fields,
        "action": action, "action_idempotency_key": uuid.uuid4(), "related": related,
    })


@login_required(login_url="/admin/login/")
def resource_action(request, resource, pk):
    if not _is_administrator(request.user) or request.method != "POST":
        raise PermissionDenied
    try:
        idempotency_key = uuid.UUID(request.POST.get("idempotency_key", ""))
    except (ValueError, TypeError, AttributeError):
        messages.error(request, _("The operation key is invalid."))
        return redirect("resource_detail", resource=resource, pk=pk)
    now = timezone.now()
    try:
        if resource == "orders":
            confirm_complete_delivery(actor=request.user, delivery_id=uuid.uuid4(), order_id=pk, delivered_at=now, idempotency_key=idempotency_key, correlation_id=request.correlation_id)
        elif resource == "payments":
            confirm_payment(actor=request.user, confirmation_id=uuid.uuid4(), payment_report_id=pk, confirmed_at=now, idempotency_key=idempotency_key, correlation_id=request.correlation_id)
        elif resource == "returns":
            confirm_return(actor=request.user, confirmation_id=uuid.uuid4(), return_report_id=pk, confirmed_at=now, idempotency_key=idempotency_key, correlation_id=request.correlation_id)
        elif resource == "commissions":
            movement = get_object_or_404(CommissionMovement, pk=pk)
            confirm_settlement(actor=request.user, settlement_id=uuid.uuid4(), seller_id=movement.seller_id, period_ends_at=now, confirmed_at=now, idempotency_key=idempotency_key, correlation_id=request.correlation_id)
        elif resource == "devices":
            device = get_object_or_404(Device, pk=pk)
            if not device.is_active:
                raise PermissionDenied
            device.is_active = False
            device.save(update_fields=["is_active", "last_seen_at"])
            AuditEvent.objects.create(actor=request.user, action="device.revoked", resource_type="device", resource_id=str(device.id), result=AuditEvent.Result.SUCCESS, source="web", correlation_id=request.correlation_id)
        elif resource == "users":
            user = get_object_or_404(get_user_model(), pk=pk)
            if user == request.user:
                raise PermissionDenied
            desired_active = request.POST.get("desired_active") == "1"
            user.is_active = desired_active
            user.save(update_fields=["is_active"])
            AuditEvent.objects.create(actor=request.user, action="user.activated" if user.is_active else "user.deactivated", resource_type="user", resource_id=str(user.id), result=AuditEvent.Result.SUCCESS, source="web", correlation_id=request.correlation_id)
        else:
            raise PermissionDenied
    except (DeliveryIdempotencyConflictError, OrderNotDeliverableError, PaymentIdempotencyConflictError, PaymentNotConfirmableError, ReturnConflictError, SettlementConflictError) as error:
        AuditEvent.objects.create(actor=request.user, action="frontend.operation_denied", resource_type=resource, resource_id=str(pk), result=AuditEvent.Result.DENIED, source="web", correlation_id=request.correlation_id, metadata={"reason": error.__class__.__name__})
        messages.error(request, _("The operation could not be completed because the record is no longer eligible."))
        return redirect("resource_detail", resource=resource, pk=pk)
    messages.success(request, _("Operation completed successfully."))
    return redirect("resource_detail", resource=resource, pk=pk)
