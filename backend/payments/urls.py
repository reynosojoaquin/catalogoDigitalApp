from django.urls import path

from .views import CommissionMovementListView, PaymentConfirmationCreateView, PaymentReportListCreateView


urlpatterns = [
    path("payments/", PaymentReportListCreateView.as_view(), name="payment-list-create"),
    path("payments/confirm/", PaymentConfirmationCreateView.as_view(), name="payment-confirm"),
    path("commissions/", CommissionMovementListView.as_view(), name="commission-list"),
]
