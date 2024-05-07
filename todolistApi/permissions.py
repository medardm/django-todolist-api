from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    The request is authenticated as a superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow non-authenticated users to view.
    """

    def has_permission(self, request, view):
        return not request.user and not request.user.is_authenticated
