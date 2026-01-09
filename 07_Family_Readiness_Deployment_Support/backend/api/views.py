"""
Family readiness platform API views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Deployment, VideoMessage, FamilyMember, Resource, EmergencyContact, ReintegrationPlan
from .serializers import (
    DeploymentSerializer, VideoMessageSerializer, FamilyMemberSerializer,
    ResourceSerializer, EmergencyContactSerializer, ReintegrationPlanSerializer
)
from datetime import date, timedelta


class DeploymentViewSet(viewsets.ModelViewSet):
    """Deployment management"""
    serializer_class = DeploymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Deployment.objects.filter(soldier=self.request.user)
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get deployment timeline with countdown"""
        deployment = self.get_object()
        today = date.today()
        
        if deployment.start_date > today:
            days_until = (deployment.start_date - today).days
            status_text = f"{days_until} days until deployment"
        elif deployment.end_date > today:
            days_remaining = (deployment.end_date - today).days
            status_text = f"{days_remaining} days remaining"
        else:
            status_text = "Deployment completed"
        
        return Response({
            "deployment": DeploymentSerializer(deployment).data,
            "status": status_text,
            "progress_percentage": self._calculate_progress(deployment)
        })
    
    def _calculate_progress(self, deployment):
        """Calculate deployment progress percentage"""
        if deployment.status == 'completed':
            return 100
        elif deployment.status == 'upcoming':
            return 0
        
        total_days = (deployment.end_date - deployment.start_date).days
        elapsed = (date.today() - deployment.start_date).days
        return min(100, max(0, int((elapsed / total_days) * 100)))


class VideoMessageViewSet(viewsets.ModelViewSet):
    """Video message management"""
    serializer_class = VideoMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        deployments = Deployment.objects.filter(soldier=self.request.user)
        return VideoMessage.objects.filter(deployment__in=deployments)
    
    @action(detail=False, methods=['post'])
    def schedule_delivery(self, request):
        """Schedule video message for future delivery"""
        deployment_id = request.data.get('deployment_id')
        scheduled_date = request.data.get('scheduled_date')
        
        # PLACEHOLDER: In production, would upload video to S3 and schedule delivery
        return Response({
            "message": "Video message scheduled",
            "scheduled_date": scheduled_date
        })


class FamilyMemberViewSet(viewsets.ModelViewSet):
    """Family member management"""
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """Resource library"""
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get resources by category"""
        category = request.query_params.get('category')
        resources = Resource.objects.filter(category=category) if category else Resource.objects.all()
        serializer = self.get_serializer(resources, many=True)
        return Response(serializer.data)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    """Emergency contact management"""
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        deployments = Deployment.objects.filter(soldier=self.request.user)
        return EmergencyContact.objects.filter(deployment__in=deployments)


class ReintegrationPlanViewSet(viewsets.ModelViewSet):
    """Reintegration planning"""
    serializer_class = ReintegrationPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        deployments = Deployment.objects.filter(soldier=self.request.user)
        return ReintegrationPlan.objects.filter(deployment__in=deployments)
