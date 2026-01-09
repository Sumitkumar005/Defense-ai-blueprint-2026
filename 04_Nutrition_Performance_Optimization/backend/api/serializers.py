"""
API serializers
"""

from rest_framework import serializers
from .models import MealPlan, Meal, HydrationLog


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class MealPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    
    class Meta:
        model = MealPlan
        fields = '__all__'


class HydrationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HydrationLog
        fields = '__all__'

