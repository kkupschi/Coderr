from rest_framework import serializers

from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Vollstaendige Darstellung einer Bestellung."""

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at',
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    """Aktualisiert nur den Status und gibt die volle Bestellung zurueck."""

    class Meta:
        model = Order
        fields = ['status']

    def to_representation(self, instance):
        return OrderSerializer(instance).data
