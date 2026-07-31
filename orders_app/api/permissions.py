from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow access only to users with a customer profile."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'customer'


class IsOrderBusinessUser(BasePermission):
    """Allow updating only for the business user of the order."""

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
