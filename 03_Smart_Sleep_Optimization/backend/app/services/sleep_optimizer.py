"""
Sleep Optimization Service
Implements two-process model of sleep regulation
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np


class SleepOptimizer:
    """Sleep optimization using two-process model"""
    
    def calculate_optimal_sleep_time(
        self,
        shift_start: datetime,
        shift_end: datetime,
        chronotype: str,
        sleep_debt: float = 0.0
    ) -> Dict:
        """
        Calculate optimal sleep time based on shift schedule
        
        Two-process model:
        - Process S: Sleep pressure (homeostatic)
        - Process C: Circadian rhythm
        """
        
        # Calculate time available for sleep
        time_until_shift = (shift_start - datetime.now()).total_seconds() / 3600
        
        # Optimal sleep duration (7-9 hours)
        target_sleep = 8.0 - sleep_debt
        
        # Calculate optimal sleep start time
        optimal_wake = shift_start - timedelta(hours=1)  # 1 hour before shift
        optimal_sleep_start = optimal_wake - timedelta(hours=target_sleep)
        
        # Adjust for chronotype
        if chronotype == "evening":
            optimal_sleep_start += timedelta(hours=1)
        elif chronotype == "morning":
            optimal_sleep_start -= timedelta(hours=1)
        
        return {
            "optimal_sleep_start": optimal_sleep_start.isoformat(),
            "optimal_wake_time": optimal_wake.isoformat(),
            "recommended_duration": target_sleep,
            "sleep_debt": sleep_debt
        }
    
    def calculate_nap_timing(
        self,
        current_time: datetime,
        next_sleep: datetime,
        alertness_level: float
    ) -> Optional[Dict]:
        """
        Calculate optimal nap timing during shift
        """
        
        time_until_sleep = (next_sleep - current_time).total_seconds() / 3600
        
        # Don't nap if less than 2 hours until sleep
        if time_until_sleep < 2:
            return None
        
        # Optimal nap: 20-30 minutes, 6-8 hours before main sleep
        nap_duration = 25  # minutes
        optimal_nap_time = next_sleep - timedelta(hours=6)
        
        if optimal_nap_time < current_time:
            return None
        
        return {
            "optimal_nap_time": optimal_nap_time.isoformat(),
            "nap_duration_minutes": nap_duration,
            "expected_alertness_boost": 0.3  # 30% boost
        }
    
    def optimize_caffeine_timing(
        self,
        shift_start: datetime,
        current_time: datetime
    ) -> Dict:
        """
        Optimize caffeine consumption timing
        """
        
        hours_until_shift = (shift_start - current_time).total_seconds() / 3600
        
        # Optimal: 1-2 hours before shift start
        optimal_caffeine_time = shift_start - timedelta(hours=1.5)
        
        # Avoid caffeine 6+ hours before sleep
        return {
            "optimal_caffeine_time": optimal_caffeine_time.isoformat(),
            "avoid_after": (shift_start - timedelta(hours=8)).isoformat(),
            "recommended_amount": "100-200mg"  # 1-2 cups coffee
        }
    
    def predict_alertness(
        self,
        sleep_history: List[Dict],
        current_time: datetime
    ) -> float:
        """
        Predict current alertness level (0-1)
        Based on sleep debt and circadian rhythm
        """
        
        # Calculate sleep debt
        total_sleep = sum(s.get("duration_hours", 0) for s in sleep_history)
        expected_sleep = 8.0 * len(sleep_history)
        sleep_debt = max(0, (expected_sleep - total_sleep) / expected_sleep)
        
        # Circadian component (simplified)
        hour = current_time.hour
        if 6 <= hour <= 10:
            circadian = 0.9  # Morning peak
        elif 14 <= hour <= 16:
            circadian = 0.7  # Afternoon dip
        elif 20 <= hour <= 22:
            circadian = 0.8  # Evening
        else:
            circadian = 0.5  # Night
        
        # Combined alertness
        alertness = circadian * (1 - sleep_debt * 0.5)
        return max(0, min(1, alertness))

