from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Erlaubt Zugriff nur fuer User mit Business-Profil."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'business'


class IsOfferOwner(BasePermission):
    """Erlaubt Bearbeiten/Loeschen nur dem Ersteller des Angebots."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
