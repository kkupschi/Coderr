from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth_app.models import UserProfile

from .permissions import IsProfileOwnerOrReadOnly
from .serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)


def build_auth_response(user):
    """Baut die einheitliche Auth-Antwort mit Token und User-Daten."""
    token, _ = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
    }


class RegistrationView(APIView):
    """Registriert einen neuen Customer- oder Business-User."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = build_auth_response(user)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authentifiziert einen User und gibt ein Token zurueck."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = build_auth_response(user)
        return Response(data, status=status.HTTP_200_OK)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Liest oder aktualisiert das Profil eines Users (pk = User-ID)."""

    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
    lookup_field = 'user'
    lookup_url_kwarg = 'pk'


class BusinessProfileListView(generics.ListAPIView):
    """Liste aller Business-Profile."""

    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')


class CustomerProfileListView(generics.ListAPIView):
    """Liste aller Customer-Profile."""

    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type='customer')
