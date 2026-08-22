from django.urls import path

from .views import ReturnConfirmationCreateView, ReturnReportListCreateView


urlpatterns = [
    path("returns/", ReturnReportListCreateView.as_view(), name="return-list-create"),
    path("returns/confirm/", ReturnConfirmationCreateView.as_view(), name="return-confirm"),
]
