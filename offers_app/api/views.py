from django.db.models import Min
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.validators import parse_decimal, parse_int
from offers_app.models import Offer, OfferDetail

from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwner
from .serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferUpdateSerializer,
)


class OfferListCreateView(generics.ListCreateAPIView):
    """List offers (filtered/ordered) or create a new one."""

    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days'),
        )
        return self._apply_filters(queryset)

    def _apply_filters(self, queryset):
        """Apply the optional query parameters, rejecting invalid values."""
        params = self.request.query_params
        creator_id = params.get('creator_id')
        min_price = params.get('min_price')
        max_delivery_time = params.get('max_delivery_time')
        if creator_id:
            queryset = queryset.filter(
                user_id=parse_int(creator_id, 'creator_id')
            )
        if min_price:
            queryset = queryset.filter(
                min_price__gte=parse_decimal(min_price, 'min_price')
            )
        if max_delivery_time:
            queryset = queryset.filter(
                min_delivery_time__lte=parse_int(
                    max_delivery_time, 'max_delivery_time'
                )
            )
        return queryset


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single offer."""

    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]


class OfferDetailSingleView(generics.RetrieveAPIView):
    """Retrieve a single detail package."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
