from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow creating only for users with a customer profile."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'customer'


class IsReviewOwner(BasePermission):
    """Allow updating/deleting only for the creator of the review."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
