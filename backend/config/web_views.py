from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
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
