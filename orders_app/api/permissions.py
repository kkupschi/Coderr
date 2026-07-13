from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Erlaubt Zugriff nur fuer User mit Customer-Profil."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'customer'


class IsOrderBusinessUser(BasePermission):
    """Erlaubt das Aktualisieren nur dem Business-User der Bestellung."""

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
