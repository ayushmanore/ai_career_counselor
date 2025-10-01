class ForwardChainingEngine:
    """
    Forward Chaining Inference Engine
    """
    
    def __init__(self, knowledge_base, fopl_engine):
        self.kb = knowledge_base
        self.fopl_engine = fopl_engine
        self.working_memory = {}
    
    def infer_careers(self, student_data):
        """
        Main inference method using forward chaining
        """
        # Initialize working memory with student facts
        self._initialize_working_memory(student_data)
        
        # Apply rules iteratively
        career_scores = {}
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            new_inferences = False
            
            # Apply FOPL rules
            for rule in self.fopl_engine.rules:
                satisfaction_level = self.fopl_engine.evaluate_conditions(rule, self.working_memory)
                
                if satisfaction_level > 0.5:  # Threshold for rule activation
                    career_name = rule.conclusion.args[0] if rule.conclusion.args else None
                    if career_name:
                        current_score = career_scores.get(career_name, 0)
                        new_score = satisfaction_level * rule.confidence
                        career_scores[career_name] = max(current_score, new_score)
                        new_inferences = True
            
            # Apply direct matching rules
            direct_matches = self._apply_direct_matching(student_data)
            for career, score in direct_matches.items():
                current_score = career_scores.get(career, 0)
                career_scores[career] = max(current_score, score)
                new_inferences = True
            
            if not new_inferences:
                break
            
            iteration += 1
        
        # Convert to recommendations
        recommendations = self._generate_recommendations(career_scores, student_data)
        return recommendations
    
    def _initialize_working_memory(self, student_data):
        """Initialize working memory with student facts"""
        self.working_memory = {}
        
        # Add subject scores
        for subject, score in student_data.get('subject_scores', {}).items():
            self.working_memory[f"score_{subject}"] = score
        
        # Infer personality traits based on subject preferences
        personality_traits = self._infer_personality_traits(student_data)
        for trait, value in personality_traits.items():
            self.working_memory[f"trait_{trait}"] = value
    
    def _infer_personality_traits(self, student_data):
        """Infer personality traits from subject scores and preferences"""
        traits = {}
        subject_scores = student_data.get('subject_scores', {})
        
        # Analyze subject performance patterns
        for trait, related_subjects in self.kb.personality_rules.items():
            trait_score = 0
            relevant_subjects = 0
            
            for subject in related_subjects:
                if subject in subject_scores:
                    trait_score += subject_scores[subject]
                    relevant_subjects += 1
            
            if relevant_subjects > 0:
                average_score = trait_score / relevant_subjects
                traits[trait] = average_score > 70  # Threshold for trait presence
        
        return traits
    
    def _apply_direct_matching(self, student_data):
        """Apply direct career matching based on subject combinations"""
        career_scores = {}
        subject_scores = student_data.get('subject_scores', {})
        
        for career_key, career_info in self.kb.careers_data.items():
            score = self._calculate_career_match_score(career_info, subject_scores)
            if score > 0:
                career_scores[career_key] = score
        
        return career_scores
    
    def _calculate_career_match_score(self, career_info, subject_scores):
        """Calculate how well a student matches a specific career"""
        required_subjects = career_info.get('required_subjects', [])
        preferred_subjects = career_info.get('preferred_subjects', [])
        min_threshold = career_info.get('min_threshold', 60)
        
        # Check required subjects
        required_score = 0
        required_count = 0
        
        for subject in required_subjects:
            if subject in subject_scores:
                score = subject_scores[subject]
                if score >= min_threshold:
                    required_score += score
                    required_count += 1
                else:
                    return 0  # Fail if any required subject is below threshold
            else:
                return 0  # Fail if required subject is missing
        
        if required_count == 0:
            return 0
        
        # Calculate average required score
        avg_required = required_score / required_count
        
        # Add bonus for preferred subjects
        preferred_bonus = 0
        for subject in preferred_subjects:
            if subject in subject_scores:
                preferred_bonus += min(subject_scores[subject] * 0.1, 10)
        
        # Final score calculation
        final_score = min((avg_required + preferred_bonus) / 100, 1.0)
        return final_score
    
    def _generate_recommendations(self, career_scores, student_data):
        """Generate final career recommendations with explanations"""
        recommendations = []
        
        # Sort careers by score
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (career_key, score) in enumerate(sorted_careers[:10]):  # Top 10
            if score > 0.3:  # Minimum threshold
                career_info = self.kb.careers_data.get(career_key, {})
                
                recommendation = {
                    'career_name': career_info.get('name', career_key.replace('_', ' ').title()),
                    'confidence_score': round(score * 100, 2),
                    'rank': i + 1,
                    'description': career_info.get('description', ''),
                    'category': career_info.get('category', 'General'),
                    'reasoning': self._generate_reasoning(career_key, career_info, student_data),
                    'required_subjects': career_info.get('required_subjects', []),
                    'preferred_subjects': career_info.get('preferred_subjects', [])
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_reasoning(self, career_key, career_info, student_data):
        """Generate explanation for why this career was recommended"""
        reasoning_parts = []
        subject_scores = student_data.get('subject_scores', {})
        
        # Check required subjects performance
        required_subjects = career_info.get('required_subjects', [])
        strong_subjects = []
        for subject in required_subjects:
            if subject in subject_scores and subject_scores[subject] >= 75:
                strong_subjects.append(subject.replace('_', ' ').title())
        
        if strong_subjects:
            reasoning_parts.append(f"Strong performance in {', '.join(strong_subjects)}")
        
        # Check preferred subjects
        preferred_subjects = career_info.get('preferred_subjects', [])
        good_preferred = []
        for subject in preferred_subjects:
            if subject in subject_scores and subject_scores[subject] >= 70:
                good_preferred.append(subject.replace('_', ' ').title())
        
        if good_preferred:
            reasoning_parts.append(f"Good aptitude in {', '.join(good_preferred)}")
        
        # Add personality match if available
        personality_match = career_info.get('personality_match', [])
        if personality_match:
            reasoning_parts.append(f"Matches personality traits: {', '.join(personality_match)}")
        
        return '. '.join(reasoning_parts) if reasoning_parts else "Based on overall academic profile"
