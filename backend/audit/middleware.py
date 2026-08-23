import uuid

from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile

from .models import AuditEvent


class AuditContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        supplied_id = request.headers.get("X-Correlation-ID", "")
        try:
            correlation_id = str(uuid.UUID(supplied_id))
        except (ValueError, AttributeError):
            correlation_id = str(uuid.uuid4())
        request.correlation_id = correlation_id
        response = self.get_response(request)
        response["X-Correlation-ID"] = correlation_id
        return response


class AdminRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/") and request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)
            if not request.user.is_superuser and (
                not request.user.is_staff or profile is None or profile.role != UserProfile.Role.ADMIN
            ):
                return HttpResponseForbidden(_("Administrator access required."))
        return self.get_response(request)


class ApiFailureAuditMiddleware:
    mutation_methods = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.path.startswith("/api/")
            and request.path != "/api/auth/token/"
            and request.method in self.mutation_methods
            and response.status_code >= 400
        ):
            actor = request.user if request.user.is_authenticated else None
            AuditEvent.objects.create(
                actor=actor,
                action="api.operation_denied",
                resource_type="api",
                result=AuditEvent.Result.DENIED,
                source="api",
                correlation_id=request.correlation_id,
                ip_address=request.META.get("REMOTE_ADDR"),
                metadata={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                },
            )
        return response


class AdminMutationAuditMiddleware:
    mutation_methods = {"POST", "PUT", "PATCH", "DELETE"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/admin/") and request.method in self.mutation_methods:
            actor = request.user if request.user.is_authenticated else None
            denied_login = request.path == "/admin/login/" and actor is None
            result = (
                AuditEvent.Result.DENIED
                if denied_login or response.status_code >= 400
                else AuditEvent.Result.SUCCESS
            )
            AuditEvent.objects.create(
                actor=actor,
                action="admin.mutation",
                resource_type="admin",
                result=result,
                source="admin",
                correlation_id=request.correlation_id,
                ip_address=request.META.get("REMOTE_ADDR"),
                metadata={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                },
            )
        return response
