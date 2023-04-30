from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role.name == "admin" else False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role.name == "user" else False
