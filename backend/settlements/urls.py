from django.urls import path

from .views import SettlementConfirmationView, SettlementListView


urlpatterns = [
    path("commission-settlements/", SettlementListView.as_view(), name="settlement-list"),
    path("commission-settlements/confirm/", SettlementConfirmationView.as_view(), name="settlement-confirm"),
]
