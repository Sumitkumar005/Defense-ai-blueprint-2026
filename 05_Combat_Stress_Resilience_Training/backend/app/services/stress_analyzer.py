"""
Stress analysis and adaptive difficulty service
"""

import numpy as np
from typing import Dict, List


class StressAnalyzer:
    """Analyze stress responses and adapt training difficulty"""
    
    def analyze_stress_response(
        self,
        baseline: Dict,
        session_data: Dict
    ) -> Dict:
        """
        Analyze stress response during training session
        
        Returns:
        - Peak stress level
        - Recovery time
        - Decision quality under stress
        - Recommendations for next session
        """
        
        heart_rate_data = session_data.get('heart_rate', [])
        hrv_data = session_data.get('hrv', [])
        
        # Calculate peak stress
        if heart_rate_data:
            peak_hr = max(heart_rate_data)
            baseline_hr = baseline.get('resting_heart_rate', 70)
            stress_ratio = (peak_hr - baseline_hr) / baseline_hr
            peak_stress = min(1.0, stress_ratio * 2)  # Normalize to 0-1
        else:
            peak_stress = 0.5
        
        # Calculate recovery time (simplified)
        recovery_time = self._calculate_recovery_time(heart_rate_data, baseline)
        
        # Decision quality (would come from VR scenario performance)
        decision_quality = session_data.get('decision_quality', 75.0)
        
        return {
            'peak_stress_level': peak_stress,
            'stress_recovery_time': recovery_time,
            'decision_quality_score': decision_quality,
            'recommendations': self._generate_recommendations(peak_stress, decision_quality)
        }
    
    def _calculate_recovery_time(self, heart_rate_data: List, baseline: Dict) -> float:
        """Calculate time to return to baseline"""
        if not heart_rate_data or len(heart_rate_data) < 2:
            return 60.0  # Default
        
        baseline_hr = baseline.get('resting_heart_rate', 70)
        threshold = baseline_hr * 1.1  # 10% above baseline
        
        # Find when HR drops below threshold
        for i, hr in enumerate(reversed(heart_rate_data)):
            if hr <= threshold:
                return len(heart_rate_data) - i
        
        return len(heart_rate_data)  # Didn't recover
    
    def _generate_recommendations(self, peak_stress: float, decision_quality: float) -> List[str]:
        """Generate recommendations based on performance"""
        recommendations = []
        
        if peak_stress > 0.8:
            recommendations.append("High stress detected - practice breathing exercises")
        
        if decision_quality < 60:
            recommendations.append("Focus on decision-making under pressure")
        
        if peak_stress < 0.3 and decision_quality > 80:
            recommendations.append("Ready for increased difficulty")
        
        return recommendations
    
    def recommend_next_difficulty(
        self,
        current_difficulty: int,
        performance_history: List[Dict]
    ) -> int:
        """
        Recommend next difficulty level using reinforcement learning
        
        PLACEHOLDER: In production, would use trained RL model
        """
        
        if not performance_history:
            return current_difficulty
        
        # Simple heuristic (would be RL model in production)
        avg_stress = np.mean([p.get('peak_stress', 0.5) for p in performance_history])
        avg_quality = np.mean([p.get('decision_quality', 75) for p in performance_history])
        
        if avg_stress < 0.4 and avg_quality > 80:
            return min(10, current_difficulty + 1)
        elif avg_stress > 0.7 or avg_quality < 60:
            return max(1, current_difficulty - 1)
        else:
            return current_difficulty

