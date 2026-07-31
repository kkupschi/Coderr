from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Allow access only to users with a business profile."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'business'


class IsOfferOwner(BasePermission):
    """Allow updating/deleting only for the creator of the offer."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
