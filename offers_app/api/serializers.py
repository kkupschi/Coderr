from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


def get_min_price(offer):
    prices = [detail.price for detail in offer.details.all()]
    return min(prices) if prices else None


def get_min_delivery_time(offer):
    times = [detail.delivery_time_in_days for detail in offer.details.all()]
    return min(times) if times else None


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Kurzform eines Detailpakets: nur ID und Link."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/offerdetails/{obj.id}/'


class OfferDetailSerializer(serializers.ModelSerializer):
    """Vollstaendiges Detailpaket."""

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
        ]


class OfferListSerializer(serializers.ModelSerializer):
    """Angebot in der Listenansicht inkl. Ersteller-Kurzinfos."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at',
            'updated_at', 'details', 'min_price', 'min_delivery_time',
            'user_details',
        ]

    def get_min_price(self, obj):
        return get_min_price(obj)

    def get_min_delivery_time(self, obj):
        return get_min_delivery_time(obj)

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Angebot in der Detailansicht (ohne user_details)."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at',
            'updated_at', 'details', 'min_price', 'min_delivery_time',
        ]

    def get_min_price(self, obj):
        return get_min_price(obj)

    def get_min_delivery_time(self, obj):
        return get_min_delivery_time(obj)


class OfferWriteResponseSerializer(serializers.ModelSerializer):
    """Antwortformat nach Erstellen/Aktualisieren: volle Detailpakete."""

    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']


class OfferCreateSerializer(serializers.ModelSerializer):
    """Erstellt ein Angebot mit genau drei Detailpaketen."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError(
                'An offer must contain exactly 3 details.'
            )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(
            user=self.context['request'].user, **validated_data
        )
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def to_representation(self, instance):
        return OfferWriteResponseSerializer(instance).data


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """Detailpaket beim Aktualisieren: offer_type identifiziert das Paket."""

    class Meta:
        model = OfferDetail
        fields = [
            'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
        ]
        extra_kwargs = {
            'title': {'required': False},
            'revisions': {'required': False},
            'delivery_time_in_days': {'required': False},
            'price': {'required': False},
            'features': {'required': False},
            'offer_type': {'required': True},
        }


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Aktualisiert ein Angebot und einzelne Detailpakete per offer_type."""

    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:
            self._update_details(instance, details_data)
        return instance

    def _update_details(self, offer, details_data):
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            detail = offer.details.get(offer_type=offer_type)
            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()

    def to_representation(self, instance):
        return OfferWriteResponseSerializer(instance).data
