"""
Family readiness platform models
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Deployment(models.Model):
    """Deployment model"""
    soldier = models.ForeignKey(User, related_name='deployments', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    timezone = models.CharField(max_length=50, default='UTC')
    status = models.CharField(
        max_length=20,
        choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('completed', 'Completed')],
        default='upcoming'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class VideoMessage(models.Model):
    """Pre-recorded video messages"""
    deployment = models.ForeignKey(Deployment, related_name='video_messages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    scheduled_delivery_date = models.DateField()
    delivered = models.BooleanField(default=False)
    recipient_type = models.CharField(
        max_length=20,
        choices=[('spouse', 'Spouse'), ('child', 'Child'), ('family', 'Family')]
    )
    created_at = models.DateTimeField(auto_now_add=True)


class FamilyMember(models.Model):
    """Family member model"""
    user = models.ForeignKey(User, related_name='family_members', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=50)  # spouse, child, parent
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class Resource(models.Model):
    """Resource library item"""
    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=[
            ('financial', 'Financial Planning'),
            ('legal', 'Legal Assistance'),
            ('childcare', 'Childcare'),
            ('mental_health', 'Mental Health'),
            ('education', 'Education'),
            ('housing', 'Housing')
        ]
    )
    description = models.TextField()
    url = models.URLField()
    contact_info = models.TextField(blank=True)


class EmergencyContact(models.Model):
    """Emergency contact during deployment"""
    deployment = models.ForeignKey(Deployment, related_name='emergency_contacts', on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    priority = models.IntegerField(default=1)  # 1 = highest


class ReintegrationPlan(models.Model):
    """Reintegration planning"""
    deployment = models.OneToOneField(Deployment, on_delete=models.CASCADE)
    counseling_scheduled = models.BooleanField(default=False)
    counseling_date = models.DateField(null=True, blank=True)
    expectations_discussed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

