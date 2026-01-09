"""
Nutrition platform API views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import MealPlan, Meal, HydrationLog, SupplementCheck
from .serializers import MealPlanSerializer, HydrationLogSerializer
from .services.nutrition_service import NutritionService
from .services.hydration_calculator import HydrationCalculator


class MealPlanViewSet(viewsets.ModelViewSet):
    """Meal plan viewset"""
    serializer_class = MealPlanSerializer
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate AI meal plan"""
        mission_type = request.data.get('mission_type', 'mixed')
        date = request.data.get('date')
        
        service = NutritionService()
        meal_plan = service.generate_meal_plan(
            user=request.user,
            mission_type=mission_type,
            date=date
        )
        
        serializer = self.get_serializer(meal_plan)
        return Response(serializer.data)


class HydrationViewSet(viewsets.ModelViewSet):
    """Hydration tracking viewset"""
    serializer_class = HydrationLogSerializer
    
    def get_queryset(self):
        return HydrationLog.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def calculate_needs(self, request):
        """Calculate hydration needs"""
        activity_level = request.data.get('activity_level', 'moderate')
        temperature = request.data.get('temperature', 20.0)
        humidity = request.data.get('humidity', 50.0)
        
        calculator = HydrationCalculator()
        recommended = calculator.calculate_hydration_needs(
            activity_level=activity_level,
            temperature=temperature,
            humidity=humidity
        )
        
        return Response({
            'recommended_intake_ml': recommended,
            'recommended_intake_oz': recommended / 29.5735
        })


class SupplementCheckViewSet(viewsets.ViewSet):
    """Supplement safety check viewset"""
    
    @action(detail=False, methods=['post'])
    def check(self, request):
        """Check supplement safety"""
        supplement_name = request.data.get('name')
        ingredients = request.data.get('ingredients', '')
        
        # PLACEHOLDER: In production, would check against DoD banned substances list
        is_safe = True  # Mock check
        warnings = []
        
        # Check for common banned substances (placeholder)
        banned_keywords = ['ephedrine', 'DMAA', 'DMHA']
        for keyword in banned_keywords:
            if keyword.lower() in ingredients.lower():
                is_safe = False
                warnings.append(f"Contains {keyword} - banned by DoD")
        
        check = SupplementCheck.objects.create(
            user=request.user,
            supplement_name=supplement_name,
            ingredients=ingredients,
            is_safe=is_safe,
            warnings='\n'.join(warnings)
        )
        
        return Response({
            'is_safe': is_safe,
            'warnings': warnings
        })

