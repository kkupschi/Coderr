from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from core.validators import parse_int
from reviews_app.models import Review

from .permissions import IsCustomerUser, IsReviewOwner
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """List reviews (filtered/ordered) or create a new one."""

    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all()
        params = self.request.query_params
        business_user_id = params.get('business_user_id')
        reviewer_id = params.get('reviewer_id')
        if business_user_id:
            queryset = queryset.filter(
                business_user_id=parse_int(
                    business_user_id, 'business_user_id'
                )
            )
        if reviewer_id:
            queryset = queryset.filter(
                reviewer_id=parse_int(reviewer_id, 'reviewer_id')
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single review."""

    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated(), IsReviewOwner()]
        return [IsAuthenticated()]
