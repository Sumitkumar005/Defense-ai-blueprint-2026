"""
API serializers
"""

from rest_framework import serializers
from .models import (
    Deployment, VideoMessage, FamilyMember, Resource,
    EmergencyContact, ReintegrationPlan
)


class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'
        read_only_fields = ('created_at',)


class VideoMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMessage
        fields = '__all__'
        read_only_fields = ('created_at',)


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'


class ReintegrationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReintegrationPlan
        fields = '__all__'
        read_only_fields = ('created_at',)
