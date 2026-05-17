from django.db import models
from django.conf import settings
from missions.models import Category


class Gig(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_APPROVED, 'Approuvé'),
        (STATUS_REJECTED, 'Rejeté'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='gigs')
    skills = models.CharField(max_length=500, blank=True, help_text='Comma-separated')
    base_rate = models.DecimalField(max_digits=8, decimal_places=2, help_text='Tarif de base (MAD)')
    delivery_days = models.PositiveIntegerField(help_text='Délai de livraison en jours')
    extras = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active'], name='gig_status_active_idx'),
            models.Index(fields=['student'], name='gig_student_idx'),
            models.Index(fields=['category'], name='gig_category_idx'),
        ]

    def __str__(self):
        return f"{self.title} — {self.student.get_full_name() or self.student.username}"

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]
