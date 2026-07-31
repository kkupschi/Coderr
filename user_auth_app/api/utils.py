"""Helper functions for building authentication responses."""

from rest_framework.authtoken.models import Token


def build_auth_response(user):
    """Build the shared auth response with token and user data."""
    token, _ = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
    }
