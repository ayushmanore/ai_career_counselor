class UncertaintyEngine:
    """
    Handles uncertainty in career recommendations using certainty factors
    """
    
    def __init__(self):
        self.certainty_factors = {}
    
    def apply_uncertainty_to_recommendations(self, recommendations):
        """
        Apply uncertainty reasoning to REDUCE overconfident scores
        """
        adjusted_recommendations = []
        
        for rec in recommendations:
            base_confidence = rec['confidence_score']
            
            # Start with the base score
            adjusted_score = base_confidence
            
            # Apply penalty for missing data
            data_penalty = self._calculate_data_penalty(rec)
            adjusted_score = adjusted_score * (1 - data_penalty)
            
            # Apply penalty for score variance
            variance_penalty = self._calculate_variance_penalty(rec)
            adjusted_score = adjusted_score * (1 - variance_penalty)
            
            # Apply general uncertainty discount (10-20% reduction)
            uncertainty_discount = 0.15  # Reduce by 15% to account for uncertainty
            adjusted_score = adjusted_score * (1 - uncertainty_discount)
            
            # Ensure score stays in reasonable range (40-90)
            final_score = max(40, min(90, adjusted_score))
            
            # Update recommendation
            adjusted_rec = rec.copy()
            adjusted_rec['confidence_score'] = int(final_score)
            adjusted_rec['uncertainty_level'] = self._categorize_uncertainty(final_score)
            
            adjusted_recommendations.append(adjusted_rec)
        
        return sorted(adjusted_recommendations, key=lambda x: x['confidence_score'], reverse=True)
    
    def _calculate_data_penalty(self, recommendation):
        """Calculate penalty for incomplete data (0.0-0.3)"""
        required_subjects = recommendation.get('required_subjects', [])
        
        if len(required_subjects) >= 3:
            return 0.05  # Small penalty with good data
        elif len(required_subjects) >= 2:
            return 0.15  # Medium penalty
        else:
            return 0.25  # Higher penalty for limited data
    
    def _calculate_variance_penalty(self, recommendation):
        """Calculate penalty for score inconsistency (0.0-0.2)"""
        confidence = recommendation['confidence_score']
        
        # Penalize very high scores more (they're likely overconfident)
        if confidence > 85:
            return 0.20  # Strong penalty for overconfidence
        elif confidence > 70:
            return 0.10  # Moderate penalty
        else:
            return 0.05  # Small penalty for lower scores
    
    def _categorize_uncertainty(self, final_score):
        """Categorize uncertainty level based on final score"""
        if final_score >= 75:
            return "Low"
        elif final_score >= 60:
            return "Medium"
        else:
            return "High"
    
    def combine_certainty_factors(self, cf1, cf2):
        """
        Simple averaging instead of Dempster-Shafer
        (The original formula was inflating scores)
        """
        return (cf1 + cf2) / 2