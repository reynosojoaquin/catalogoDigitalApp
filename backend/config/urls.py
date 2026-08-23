from django.contrib import admin
from django.urls import include, path

from .views import health
from .web_views import dashboard, resource_action, resource_detail, resource_list

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("dashboard/", dashboard, name="dashboard"),
    path("app/<slug:resource>/", resource_list, name="resource_list"),
    path("app/<slug:resource>/<uuid:pk>/", resource_detail, name="resource_detail"),
    path("app/<slug:resource>/<uuid:pk>/action/", resource_action, name="resource_action"),
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
