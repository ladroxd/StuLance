from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_CLIENT = 'client'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_STUDENT, _('Student')),
        (ROLE_CLIENT, _('Recruiter')),
        (ROLE_ADMIN, _('Administrator')),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_student(self):
        return self.role == self.ROLE_STUDENT

    def is_client(self):
        return self.role == self.ROLE_CLIENT


class StudentProfile(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_VERIFIED = 'verified'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_VERIFIED, _('Verified')),
        (STATUS_REJECTED, _('Rejected')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/students/', blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, help_text=_('Comma-separated tags'))
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    school = models.CharField(max_length=200, blank=True)
    field_of_study = models.CharField(max_length=200, blank=True)
    student_card = models.FileField(upload_to='student_cards/', blank=True, null=True)
    verification_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    average_rating = models.FloatField(default=0.0)
    total_missions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class PortfolioProject(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClientProfile(models.Model):
    TYPE_COMPANY = 'company'
    TYPE_INDIVIDUAL = 'individual'
    TYPE_CHOICES = [
        (TYPE_COMPANY, _('Company')),
        (TYPE_INDIVIDUAL, _('Individual')),
    ]

    class Meta:
        verbose_name = _('Recruiter Profile')
        verbose_name_plural = _('Recruiter Profiles')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    client_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default=TYPE_INDIVIDUAL)
    company_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profiles/clients/', blank=True, null=True)
    website = models.URLField(blank=True)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.company_name or self.user.get_full_name() or self.user.username
