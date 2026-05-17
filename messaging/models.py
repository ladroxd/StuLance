from django.db import models
from django.conf import settings
from missions.models import Mission


class Message(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['mission', 'is_read'], name='message_mission_read_idx'),
        ]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class DirectConversation(models.Model):
    participant1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_p1')
    participant2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_p2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('participant1', 'participant2')]
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['participant1', '-updated_at'], name='conv_p1_updated_idx'),
            models.Index(fields=['participant2', '-updated_at'], name='conv_p2_updated_idx'),
        ]

    def other_participant(self, user):
        return self.participant2 if self.participant1 == user else self.participant1

    def unread_count(self, user):
        return self.direct_messages.filter(is_read=False).exclude(sender=user).count()

    @classmethod
    def get_or_create_between(cls, user_a, user_b):
        # always store with lower pk as participant1 to avoid duplicates
        p1, p2 = (user_a, user_b) if user_a.pk < user_b.pk else (user_b, user_a)
        conv, created = cls.objects.get_or_create(participant1=p1, participant2=p2)
        return conv

    def __str__(self):
        return f"{self.participant1.username} ↔ {self.participant2.username}"


class DirectMessage(models.Model):
    conversation = models.ForeignKey(DirectConversation, on_delete=models.CASCADE, related_name='direct_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='direct_sent')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'is_read'], name='dmessage_conv_read_idx'),
        ]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
