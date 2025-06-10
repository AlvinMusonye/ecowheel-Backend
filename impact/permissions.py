
from rest_framework import permissions

class IsOwnerOrSystem(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        return request.user and request.user.is_staff
