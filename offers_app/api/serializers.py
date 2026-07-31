from rest_framework import serializers

from offers_app.models import Offer, OfferDetail

from .utils import get_min_delivery_time, get_min_price


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Short form of a detail package: id and link only."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/offerdetails/{obj.id}/'


class OfferDetailSerializer(serializers.ModelSerializer):
    """Full detail package."""

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type',
        ]


class OfferListSerializer(serializers.ModelSerializer):
    """Offer in list view including short creator info."""

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
    """Offer in detail view (without user_details)."""

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
    """Response format after create/update: full detail packages."""

    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']


class OfferCreateSerializer(serializers.ModelSerializer):
    """Create an offer with exactly three detail packages."""

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
    """Detail package on update: offer_type identifies the package."""

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
    """Update an offer and individual detail packages by offer_type."""

    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        """Ensure every entry names an offer_type the offer actually has.

        A PATCH makes the nested serializer partial, which silently drops the
        required flag on offer_type, so the check has to happen here.
        """
        seen = set()
        for detail_data in value:
            offer_type = detail_data.get('offer_type')
            if not offer_type:
                raise serializers.ValidationError(
                    'Each detail requires an offer_type.'
                )
            if offer_type in seen:
                raise serializers.ValidationError(
                    f'Duplicate offer_type "{offer_type}".'
                )
            if not self.instance.details.filter(
                offer_type=offer_type
            ).exists():
                raise serializers.ValidationError(
                    f'This offer has no detail of type "{offer_type}".'
                )
            seen.add(offer_type)
        return value

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
            detail = offer.details.get(
                offer_type=detail_data['offer_type']
            )
            for attr, value in detail_data.items():
                setattr(detail, attr, value)
            detail.save()

    def to_representation(self, instance):
        return OfferWriteResponseSerializer(instance).data
