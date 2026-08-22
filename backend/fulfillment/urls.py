from django.urls import path

from .views import DeliveryConfirmationView, InvoiceListView


urlpatterns = [
    path("deliveries/complete/", DeliveryConfirmationView.as_view(), name="delivery-complete"),
    path("invoices/", InvoiceListView.as_view(), name="invoice-list"),
]
