from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.validators import parse_int
from offers_app.models import OfferDetail
from orders_app.models import Order
from user_auth_app.models import UserProfile

from .permissions import IsCustomerUser, IsOrderBusinessUser
from .serializers import OrderSerializer, OrderStatusSerializer
from .utils import create_order_from_detail


class OrderListCreateView(generics.ListCreateAPIView):
    """List the user's own orders or create a new one."""

    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def create(self, request, *args, **kwargs):
        offer_detail_id = request.data.get('offer_detail_id')
        if not offer_detail_id:
            return Response(
                {'offer_detail_id': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        offer_detail = get_object_or_404(
            OfferDetail, id=parse_int(offer_detail_id, 'offer_detail_id')
        )
        order = create_order_from_detail(offer_detail, request.user)
        return Response(
            OrderSerializer(order).data, status=status.HTTP_201_CREATED
        )


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update the status of, or delete an order."""

    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return OrderStatusSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated(), IsOrderBusinessUser()]
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]


class OrderCountView(APIView):
    """Number of running orders of a business user."""

    def get(self, request, business_user_id):
        get_object_or_404(
            UserProfile, user_id=business_user_id, type='business'
        )
        count = Order.objects.filter(
            business_user_id=business_user_id, status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    """Number of completed orders of a business user."""

    def get(self, request, business_user_id):
        get_object_or_404(
            UserProfile, user_id=business_user_id, type='business'
        )
        count = Order.objects.filter(
            business_user_id=business_user_id, status='completed'
        ).count()
        return Response({'completed_order_count': count})
