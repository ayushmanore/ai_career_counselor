class KnowledgeBase:
    """
    Knowledge Base containing facts, rules, and career information
    """
    
    def __init__(self):
        self.facts = {}
        self.rules = []
        self.careers_data = self._initialize_careers()
        self.subjects_data = self._initialize_subjects()
        self.personality_rules = self._initialize_personality_rules()
    
    def _initialize_subjects(self):
        return {
            'mathematics': {'category': 'STEM', 'weight': 1.2, 'related_skills': ['analytical', 'logical']},
            'physics': {'category': 'STEM', 'weight': 1.2, 'related_skills': ['analytical', 'problem_solving']},
            'chemistry': {'category': 'STEM', 'weight': 1.1, 'related_skills': ['analytical', 'detail_oriented']},
            'biology': {'category': 'STEM', 'weight': 1.1, 'related_skills': ['analytical', 'caring']},
            'computer_science': {'category': 'STEM', 'weight': 1.3, 'related_skills': ['logical', 'creative']},
            'english': {'category': 'Language', 'weight': 1.0, 'related_skills': ['communication', 'creative']},
            'history': {'category': 'Social', 'weight': 0.9, 'related_skills': ['analytical', 'research']},
            'geography': {'category': 'Social', 'weight': 0.9, 'related_skills': ['analytical', 'environmental']},
            'economics': {'category': 'Commerce', 'weight': 1.1, 'related_skills': ['analytical', 'business']},
            'business_studies': {'category': 'Commerce', 'weight': 1.0, 'related_skills': ['leadership', 'business']},
            'art': {'category': 'Creative', 'weight': 0.8, 'related_skills': ['creative', 'visual']},
            'music': {'category': 'Creative', 'weight': 0.8, 'related_skills': ['creative', 'artistic']},
            'physical_education': {'category': 'Sports', 'weight': 0.7, 'related_skills': ['physical', 'leadership']}
        }
    
    def _initialize_careers(self):
        return {
            'software_engineer': {
                'name': 'Software Engineer',
                'required_subjects': ['mathematics', 'computer_science', 'physics'],
                'preferred_subjects': ['english'],
                'min_threshold': 75,
                'personality_match': ['logical', 'creative', 'problem_solving'],
                'category': 'Technology',
                'description': 'Design and develop software applications and systems'
            },
            'data_scientist': {
                'name': 'Data Scientist',
                'required_subjects': ['mathematics', 'computer_science'],
                'preferred_subjects': ['physics', 'economics'],
                'min_threshold': 80,
                'personality_match': ['analytical', 'logical', 'research'],
                'category': 'Technology',
                'description': 'Analyze complex data to help organizations make decisions'
            },
            'doctor': {
                'name': 'Medical Doctor',
                'required_subjects': ['biology', 'chemistry', 'physics'],
                'preferred_subjects': ['mathematics'],
                'min_threshold': 85,
                'personality_match': ['caring', 'detail_oriented', 'problem_solving'],
                'category': 'Healthcare',
                'description': 'Diagnose and treat patients, promote health and wellness'
            },
            'engineer': {
                'name': 'Engineer',
                'required_subjects': ['mathematics', 'physics'],
                'preferred_subjects': ['chemistry', 'computer_science'],
                'min_threshold': 75,
                'personality_match': ['analytical', 'problem_solving', 'logical'],
                'category': 'Engineering',
                'description': 'Design, build, and maintain structures, machines, or systems'
            },
            'teacher': {
                'name': 'Teacher',
                'required_subjects': ['english'],
                'preferred_subjects': ['any_high_score_subject'],
                'min_threshold': 70,
                'personality_match': ['communication', 'caring', 'leadership'],
                'category': 'Education',
                'description': 'Educate and inspire students in various subjects'
            },
            'business_analyst': {
                'name': 'Business Analyst',
                'required_subjects': ['economics', 'business_studies', 'mathematics'],
                'preferred_subjects': ['computer_science'],
                'min_threshold': 70,
                'personality_match': ['analytical', 'business', 'communication'],
                'category': 'Business',
                'description': 'Analyze business processes and recommend improvements'
            },
            'graphic_designer': {
                'name': 'Graphic Designer',
                'required_subjects': ['art'],
                'preferred_subjects': ['computer_science', 'english'],
                'min_threshold': 65,
                'personality_match': ['creative', 'visual', 'artistic'],
                'category': 'Creative',
                'description': 'Create visual concepts to communicate ideas and inspire audiences'
            },
            'psychologist': {
                'name': 'Psychologist',
                'required_subjects': ['biology'],
                'preferred_subjects': ['english', 'history'],
                'min_threshold': 75,
                'personality_match': ['caring', 'communication', 'analytical'],
                'category': 'Healthcare',
                'description': 'Study behavior and mental processes to help people'
            },
            'financial_analyst': {
                'name': 'Financial Analyst',
                'required_subjects': ['mathematics', 'economics'],
                'preferred_subjects': ['business_studies', 'computer_science'],
                'min_threshold': 75,
                'personality_match': ['analytical', 'detail_oriented', 'business'],
                'category': 'Finance',
                'description': 'Evaluate investment opportunities and financial data'
            },
            'journalist': {
                'name': 'Journalist',
                'required_subjects': ['english'],
                'preferred_subjects': ['history', 'geography'],
                'min_threshold': 70,
                'personality_match': ['communication', 'research', 'creative'],
                'category': 'Media',
                'description': 'Research, write, and report news and feature stories'
            }
        }
    
    def _initialize_personality_rules(self):
        return {
            'analytical': ['mathematics', 'physics', 'chemistry', 'economics'],
            'creative': ['art', 'music', 'english', 'computer_science'],
            'logical': ['mathematics', 'computer_science', 'physics'],
            'caring': ['biology', 'physical_education'],
            'communication': ['english', 'history'],
            'leadership': ['business_studies', 'physical_education'],
            'problem_solving': ['mathematics', 'physics', 'computer_science'],
            'detail_oriented': ['chemistry', 'biology'],
            'business': ['economics', 'business_studies'],
            'research': ['history', 'geography'],
            'visual': ['art'],
            'artistic': ['art', 'music'],
            'physical': ['physical_education'],
            'environmental': ['geography', 'biology']
        }
    
    def add_fact(self, fact_name, fact_value):
        """Add a fact to the knowledge base"""
        self.facts[fact_name] = fact_value
    
    def get_fact(self, fact_name):
        """Retrieve a fact from the knowledge base"""
        return self.facts.get(fact_name)
    
    def add_rule(self, rule):
        """Add a rule to the knowledge base"""
        self.rules.append(rule)
