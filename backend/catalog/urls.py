from django.urls import path

from .views import CustomerListCreateView, ProductListView


urlpatterns = [
    path("customers/", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("products/", ProductListView.as_view(), name="product-list"),
]
