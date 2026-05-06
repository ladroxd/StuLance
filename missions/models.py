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


class Report(models.Model):
    REASON_SPAM = 'spam'
    REASON_INAPPROPRIATE = 'inappropriate'
    REASON_FAKE = 'fake'
    REASON_OTHER = 'other'
    REASON_CHOICES = [
        (REASON_SPAM, 'Spam ou arnaque'),
        (REASON_INAPPROPRIATE, 'Contenu inapproprie'),
        (REASON_FAKE, 'Faux profil / fausse mission'),
        (REASON_OTHER, 'Autre'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_REVIEWED = 'reviewed'
    STATUS_DISMISSED = 'dismissed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_REVIEWED, 'Traite'),
        (STATUS_DISMISSED, 'Rejete'),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reported_mission = models.ForeignKey(Mission, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_received')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True, help_text='Details supplementaires (optionnel)')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.reported_mission or self.reported_user
        return f"Signalement de {self.reporter.username} → {target}"


class Submission(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REVISION = 'revision'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_ACCEPTED, 'Accepte'),
        (STATUS_REVISION, 'Revision demandee'),
    ]

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    link = models.URLField(blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Livraison de {self.student.username} pour {self.mission.title}"


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
