from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    """A review of a business user written by a customer."""

    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received'
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_written'
    )
    rating = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
        ordering = ['-updated_at']

    def __str__(self):
        return f'Review {self.rating} by {self.reviewer.username}'
