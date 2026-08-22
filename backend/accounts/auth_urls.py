from django.urls import path

from .auth_views import AuditedAuthTokenView


urlpatterns = [
    path("token/", AuditedAuthTokenView.as_view(), name="api-token"),
]
