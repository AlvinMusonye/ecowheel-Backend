from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Full access for admins. Read-only for all other authenticated users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    - List views: Any authenticated user is allowed.
    - Object-level views: Only the owner or an admin can access/modify.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin always has permission
        if request.user.is_authenticated and request.user.role == 'admin':
            return True

        # Check for ownership based on object type
        if isinstance(obj, UserProfile): # For UserProfile objects
            return obj.user == request.user
        elif isinstance(obj, User): # For User objects
            return obj == request.user
        return False


class IsAdminOrOperator(permissions.BasePermission):
    """
    Grants access only to users with 'admin' or 'operator' role.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'operator']
        )

class IsAdminOnly(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'
