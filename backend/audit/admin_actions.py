from accounts.models import UserProfile


class DomainActionAdminMixin:
    def has_administer_permission(self, request):
        user = request.user
        if not user.is_active or not user.is_staff:
            return False
        if user.is_superuser:
            return True
        role = getattr(getattr(user, "profile", None), "role", None)
        permission = f"{self.opts.app_label}.change_{self.opts.model_name}"
        return role == UserProfile.Role.ADMIN and user.has_perm(permission)

    @staticmethod
    def correlation_id(request):
        return request.correlation_id
