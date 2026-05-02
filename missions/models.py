from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Mission(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Ouverte'),
        (STATUS_IN_PROGRESS, 'En cours'),
        (STATUS_COMPLETED, 'Terminee'),
        (STATUS_CANCELLED, 'Annulee'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='missions')
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='missions')
    skills_required = models.CharField(max_length=500, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline_days = models.PositiveIntegerField(help_text='Duree en jours')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_OPEN)
    selected_student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='active_missions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_ACCEPTED, 'Acceptee'),
        (STATUS_REJECTED, 'Refusee'),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mission', 'student')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.username} -> {self.mission.title}"


class Review(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mission', 'reviewer')

    def __str__(self):
        return f"Avis de {self.reviewer.username} pour {self.reviewee.username}"
