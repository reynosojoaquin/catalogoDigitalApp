from django.urls import path

from .views import BusinessChangeFeedView, CatalogChangeFeedView, CursorAcknowledgementView, SyncBatchView, SyncCustomerOperationView


urlpatterns = [
    path("sync/customer-operations/", SyncCustomerOperationView.as_view(), name="sync-customer-operation"),
    path("sync/catalog-changes/", CatalogChangeFeedView.as_view(), name="sync-catalog-changes"),
    path("sync/business-changes/", BusinessChangeFeedView.as_view(), name="sync-business-changes"),
    path("sync/cursor/ack/", CursorAcknowledgementView.as_view(), name="sync-cursor-ack"),
    path("sync/batch/", SyncBatchView.as_view(), name="sync-batch"),
]
