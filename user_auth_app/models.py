from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Additional data for a user (customer or business partner)."""

    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['user__username']

    def __str__(self):
        return f'{self.user.username} ({self.type})'
