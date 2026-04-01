from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Allow access only to authenticated ADMIN users."""

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsReadOnlyOrAdminWrite(permissions.BasePermission):
    """Allow read-only for authenticated users, write only for ADMIN."""

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == 'ADMIN'


class IsAnalystOrAdmin(permissions.BasePermission):
    """Allow analytics endpoints for ANALYST and ADMIN users."""

    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {'ANALYST', 'ADMIN'}
        )
