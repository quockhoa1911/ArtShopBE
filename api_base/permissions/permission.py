from rest_framework.permissions import BasePermission

ANONYMOUS = "anonymous"


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        action = view.action
        scope_of_action = view.scopes.get(action)

        if scope_of_action:
            if scope_of_action == ANONYMOUS: return True
            return True if request.user.role.name in scope_of_action else False
        return True if request.user.role.name == "admin" else False


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        action = view.action
        scope_of_action = view.scopes.get(action)
        if scope_of_action:
            if scope_of_action == ANONYMOUS: return True
            return True if request.user.role.name in scope_of_action else False

        return True if request.user.role.name == "user" else False
