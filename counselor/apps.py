from django.apps import AppConfig

class CounselorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'counselor'
    verbose_name = 'AI Career Counselor'
    
    def ready(self):
        # Initialize AI components when app starts
        from .ai_engine.knowledge_base import KnowledgeBase
        from .ai_engine.fopl_rules import FOPLRuleEngine
        
        # Pre-load knowledge base for better performance
        kb = KnowledgeBase()
        fopl_engine = FOPLRuleEngine(kb)
