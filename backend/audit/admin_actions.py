from accounts.models import UserProfile


class AdminRoleRequiredMixin:
    def _has_admin_role(self, request):
        user = request.user
        if not user.is_active or not user.is_staff:
            return False
        return user.is_superuser or getattr(getattr(user, "profile", None), "role", None) == UserProfile.Role.ADMIN

    def has_module_permission(self, request):
        return self._has_admin_role(request)

    def has_view_permission(self, request, obj=None):
        if not self._has_admin_role(request):
            return False
        user = request.user
        return user.is_superuser or user.has_perm(f"{self.opts.app_label}.view_{self.opts.model_name}")

    def has_add_permission(self, request):
        if not self._has_admin_role(request):
            return False
        return request.user.is_superuser or request.user.has_perm(f"{self.opts.app_label}.add_{self.opts.model_name}")

    def has_change_permission(self, request, obj=None):
        if not self._has_admin_role(request):
            return False
        return request.user.is_superuser or request.user.has_perm(f"{self.opts.app_label}.change_{self.opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        if not self._has_admin_role(request):
            return False
        return request.user.is_superuser or request.user.has_perm(f"{self.opts.app_label}.delete_{self.opts.model_name}")


class DomainActionAdminMixin(AdminRoleRequiredMixin):
    def has_administer_permission(self, request):
        if not self._has_admin_role(request):
            return False
        user = request.user
        if user.is_superuser:
            return True
        permission = f"{self.opts.app_label}.change_{self.opts.model_name}"
        return user.has_perm(permission)

    @staticmethod
    def correlation_id(request):
        return request.correlation_id
