from rest_framework import serializers

from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Full representation of an order."""

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at',
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    """Update the status only and return the full order."""

    class Meta:
        model = Order
        fields = ['status']

    def to_representation(self, instance):
        return OrderSerializer(instance).data
