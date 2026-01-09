"""
Nutrition recommendation service
"""

from ..models import MealPlan, Meal
from datetime import date


class NutritionService:
    """Service for nutrition recommendations"""
    
    MISSION_NUTRITION_PROFILES = {
        'endurance': {
            'calories': 3000,
            'protein_ratio': 0.15,
            'carbs_ratio': 0.60,
            'fat_ratio': 0.25
        },
        'strength': {
            'calories': 3200,
            'protein_ratio': 0.30,
            'carbs_ratio': 0.45,
            'fat_ratio': 0.25
        },
        'cognitive': {
            'calories': 2800,
            'protein_ratio': 0.20,
            'carbs_ratio': 0.50,
            'fat_ratio': 0.30
        },
        'mixed': {
            'calories': 3000,
            'protein_ratio': 0.20,
            'carbs_ratio': 0.55,
            'fat_ratio': 0.25
        }
    }
    
    def generate_meal_plan(self, user, mission_type, date=None):
        """Generate personalized meal plan"""
        if date is None:
            date = date.today()
        
        profile = self.MISSION_NUTRITION_PROFILES.get(mission_type, self.MISSION_NUTRITION_PROFILES['mixed'])
        
        meal_plan = MealPlan.objects.create(
            user=user,
            date=date,
            mission_type=mission_type,
            total_calories=profile['calories'],
            protein_grams=profile['calories'] * profile['protein_ratio'] / 4,
            carbs_grams=profile['calories'] * profile['carbs_ratio'] / 4,
            fat_grams=profile['calories'] * profile['fat_ratio'] / 9
        )
        
        # Generate meals (placeholder - would use ML recommendation)
        self._generate_meals(meal_plan, profile)
        
        return meal_plan
    
    def _generate_meals(self, meal_plan, profile):
        """Generate individual meals"""
        # Placeholder: In production, would use collaborative filtering
        # to recommend meals from DFAC menu or MRE database
        
        meals_data = [
            {
                'meal_type': 'breakfast',
                'name': 'DFAC Breakfast Plate',
                'calories': 600,
                'protein': 30,
                'carbs': 70,
                'fat': 20,
                'source': 'dfac'
            },
            {
                'meal_type': 'lunch',
                'name': 'DFAC Lunch Plate',
                'calories': 800,
                'protein': 50,
                'carbs': 90,
                'fat': 25,
                'source': 'dfac'
            },
            {
                'meal_type': 'dinner',
                'name': 'DFAC Dinner Plate',
                'calories': 900,
                'protein': 60,
                'carbs': 100,
                'fat': 30,
                'source': 'dfac'
            },
            {
                'meal_type': 'snack',
                'name': 'Protein Bar',
                'calories': 200,
                'protein': 20,
                'carbs': 25,
                'fat': 5,
                'source': 'custom'
            }
        ]
        
        for meal_data in meals_data:
            Meal.objects.create(meal_plan=meal_plan, **meal_data)

