from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwnerOrReadOnly(BasePermission):
    """Allow editing only for the owner, reading for everyone."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
