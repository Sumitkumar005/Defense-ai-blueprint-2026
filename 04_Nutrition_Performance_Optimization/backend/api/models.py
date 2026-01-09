"""
Nutrition platform models
"""

from django.db import models
from django.contrib.auth.models import User


class MealPlan(models.Model):
    """Meal plan model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mission_type = models.CharField(max_length=50)  # endurance, strength, cognitive
    total_calories = models.IntegerField()
    protein_grams = models.FloatField()
    carbs_grams = models.FloatField()
    fat_grams = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Meal(models.Model):
    """Individual meal model"""
    meal_plan = models.ForeignKey(MealPlan, related_name='meals', on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20)  # breakfast, lunch, dinner, snack
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    source = models.CharField(max_length=50)  # dfac, mre, custom


class HydrationLog(models.Model):
    """Hydration tracking model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    water_intake_ml = models.IntegerField()
    activity_level = models.CharField(max_length=20)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    recommended_intake_ml = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)


class SupplementCheck(models.Model):
    """Supplement safety check model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplement_name = models.CharField(max_length=200)
    ingredients = models.TextField()
    is_safe = models.BooleanField()
    warnings = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)


class PerformanceCorrelation(models.Model):
    """Nutrition-performance correlation model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    nutrition_score = models.FloatField()  # 0-100
    pt_score = models.FloatField(null=True)
    mission_performance = models.FloatField(null=True)
    correlation_data = models.JSONField(default=dict)

