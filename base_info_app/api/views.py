from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from reviews_app.models import Review
from user_auth_app.models import UserProfile


class BaseInfoView(APIView):
    """Allgemeine Plattform-Statistiken (oeffentlich)."""

    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        average = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        data = {
            'review_count': review_count,
            'average_rating': round(average, 1),
            'business_profile_count': UserProfile.objects.filter(
                type='business'
            ).count(),
            'offer_count': Offer.objects.count(),
        }
        return Response(data)
