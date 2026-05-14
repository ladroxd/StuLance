from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_APPLICATION = 'application'
    TYPE_MESSAGE = 'message'
    TYPE_MISSION_ACCEPTED = 'mission_accepted'
    TYPE_MISSION_COMPLETED = 'mission_completed'
    TYPE_CHOICES = [
        (TYPE_APPLICATION, 'New application'),
        (TYPE_MESSAGE, 'New message'),
        (TYPE_MISSION_ACCEPTED, 'Application accepted'),
        (TYPE_MISSION_COMPLETED, 'Mission completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # Legacy fields — kept for old notifications that pre-date the key system
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)

    # Key-based translation fields
    title_key = models.CharField(max_length=100, blank=True)
    message_key = models.CharField(max_length=100, blank=True)
    params = models.JSONField(default=dict, blank=True)

    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title_key or self.title}"
