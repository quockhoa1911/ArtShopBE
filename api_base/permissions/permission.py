from rest_framework.permissions import BasePermission

ANONYMOUS = "anonymous"
ADMIN = "admin"
USER = "user"


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        action = view.action
        scope_of_action = view.scopes.get(action)

        if not request.user.is_anonymous and request.user.role and request.user.role.name == ADMIN: return True

        if scope_of_action:
            if ANONYMOUS in scope_of_action: return True
            if not request.user.is_anonymous and request.user.role and request.user.role.name in scope_of_action: return True
        return False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        action = view.action
        scope_of_action = view.scopes.get(action)

        if not request.user.is_anonymous and request.user.role and request.user.role.name == USER: return True

        if scope_of_action:
            if ANONYMOUS in scope_of_action: return True
            if not request.user.is_anonymous and request.user.role and request.user.role.name in scope_of_action: return True
        return False
