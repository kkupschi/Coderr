from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Read/create a review (at most one per business and reviewer)."""

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            already_exists = Review.objects.filter(
                business_user=attrs.get('business_user'),
                reviewer=request.user,
            ).exists()
            if already_exists:
                raise serializers.ValidationError(
                    'You have already reviewed this business.'
                )
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Update the rating and description of a review only."""

    class Meta:
        model = Review
        fields = [
            'id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'business_user', 'reviewer', 'created_at', 'updated_at',
        ]
