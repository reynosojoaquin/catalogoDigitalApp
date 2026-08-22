from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _

from .models import UserProfile


class IsSeller(BasePermission):
    message = _("A seller account is required.")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_active:
            return False

        return UserProfile.objects.filter(
            user=request.user,
            role=UserProfile.Role.SELLER,
        ).exists()


class IsAdministrator(BasePermission):
    message = _("An administrator account is required.")

    def has_permission(self, request, view):
        if not request.user or not request.user.is_active:
            return False
        if request.user.is_superuser:
            return True

        return UserProfile.objects.filter(
            user=request.user,
            role=UserProfile.Role.ADMIN,
        ).exists()
