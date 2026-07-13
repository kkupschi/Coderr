from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Erlaubt das Erstellen nur fuer User mit Customer-Profil."""

    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile is not None and profile.type == 'customer'


class IsReviewOwner(BasePermission):
    """Erlaubt Bearbeiten/Loeschen nur dem Ersteller der Bewertung."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
