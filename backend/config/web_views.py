from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _

from accounts.models import Device, UserProfile
from audit.models import AuditEvent
from catalog.models import Customer, Product
from fulfillment.models import Invoice
from payments.models import CommissionMovement, PaymentReport
from returns.models import ReturnReport
from sales.models import Order


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
            {"label": _("Active products"), "value": Product.objects.filter(is_active=True).count(), "url": "/admin/catalog/product/"},
            {"label": _("Active customers"), "value": Customer.objects.filter(is_active=True).count(), "url": "/admin/catalog/customer/"},
            {"label": _("Submitted orders"), "value": Order.objects.filter(status=Order.Status.SUBMITTED).count(), "url": "/admin/sales/order/?status=submitted"},
            {"label": _("Unpaid invoices"), "value": Invoice.objects.filter(status=Invoice.Status.UNPAID).count(), "url": "/admin/fulfillment/invoice/?status=unpaid"},
            {"label": _("Reported payments"), "value": PaymentReport.objects.filter(status=PaymentReport.Status.REPORTED).count(), "url": "/admin/payments/paymentreport/?status=reported"},
            {"label": _("Reported returns"), "value": ReturnReport.objects.filter(status=ReturnReport.Status.REPORTED).count(), "url": "/admin/returns/returnreport/?status=reported"},
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
    rows = [[_value_for_column(item, field) for field, _ in config["columns"]] for item in page]
    statuses = []
    if hasattr(config["model"], "Status"):
        statuses = [(choice.value, choice.label) for choice in config["model"].Status]
    return render(request, "dashboard/resource_list.html", {
        "page_title": config["title"], "columns": [label for _, label in config["columns"]],
        "rows": rows, "page_obj": page, "query": query, "statuses": statuses,
        "status_filter": status_filter, "resource": resource,
    })
