from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_superuser
