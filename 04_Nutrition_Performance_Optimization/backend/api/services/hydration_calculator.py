"""
Hydration needs calculator
"""

class HydrationCalculator:
    """Calculate hydration needs based on activity and environment"""
    
    BASE_HYDRATION_ML = 2000  # Base daily need
    
    ACTIVITY_MULTIPLIERS = {
        'light': 1.0,
        'moderate': 1.3,
        'intense': 1.6,
        'extreme': 2.0
    }
    
    def calculate_hydration_needs(
        self,
        activity_level='moderate',
        temperature=20.0,
        humidity=50.0,
        duration_hours=8.0
    ):
        """
        Calculate hydration needs in ml
        
        Factors:
        - Base metabolic need
        - Activity level
        - Temperature (sweat loss)
        - Humidity (affects sweat evaporation)
        - Duration of activity
        """
        
        base = self.BASE_HYDRATION_ML
        activity_mult = self.ACTIVITY_MULTIPLIERS.get(activity_level, 1.3)
        
        # Temperature adjustment (sweat loss increases with heat)
        temp_adjustment = 0
        if temperature > 25:
            temp_adjustment = (temperature - 25) * 50  # 50ml per degree above 25C
        
        # Humidity adjustment (high humidity = less evaporation = more sweat)
        humidity_adjustment = 0
        if humidity > 70:
            humidity_adjustment = (humidity - 70) * 2
        
        # Calculate total
        total_ml = (base * activity_mult) + temp_adjustment + humidity_adjustment
        
        # Adjust for activity duration
        total_ml = total_ml * (duration_hours / 8.0)
        
        return int(total_ml)

