from django.contrib import admin
from django.urls import include, path

from .views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.auth_urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("catalog.urls")),
    path("api/", include("sales.urls")),
    path("api/", include("fulfillment.urls")),
    path("api/", include("payments.urls")),
    path("api/", include("returns.urls")),
    path("api/", include("settlements.urls")),
    path("api/", include("sync.urls")),
    path("health/", health, name="health"),
]
