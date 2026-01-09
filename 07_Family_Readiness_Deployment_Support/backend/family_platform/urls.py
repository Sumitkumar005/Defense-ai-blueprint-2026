"""
URL configuration
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    DeploymentViewSet, VideoMessageViewSet, FamilyMemberViewSet,
    ResourceViewSet, EmergencyContactViewSet, ReintegrationPlanViewSet
)

router = DefaultRouter()
router.register(r'deployments', DeploymentViewSet)
router.register(r'video-messages', VideoMessageViewSet)
router.register(r'family-members', FamilyMemberViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'emergency-contacts', EmergencyContactViewSet)
router.register(r'reintegration-plans', ReintegrationPlanViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

