import os
from django.core.management.base import BaseCommand
from counselor.models import Subject, Career
from counselor.ai_engine.knowledge_base import KnowledgeBase

class Command(BaseCommand):
    help = 'Populate database with initial career and subject data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing entries',
        )
    
    def handle(self, *args, **options):
        kb = KnowledgeBase()
        force_update = options['force']
        
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create subjects
        subjects_created = 0
        subjects_updated = 0
        
        for subject_code, subject_info in kb.subjects_data.items():
            subject_name = subject_code.replace('_', ' ').title()
            
            if force_update:
                subject, created = Subject.objects.update_or_create(
                    name=subject_name,
                    defaults={
                        'category': subject_info['category'],
                        'weight': subject_info['weight']
                    }
                )
                if created:
                    subjects_created += 1
                else:
                    subjects_updated += 1
            else:
                subject, created = Subject.objects.get_or_create(
                    name=subject_name,
                    defaults={
                        'category': subject_info['category'],
                        'weight': subject_info['weight']
                    }
                )
                if created:
                    subjects_created += 1
        
        self.stdout.write(f'Subjects: {subjects_created} created, {subjects_updated} updated')
        
        # Create careers
        careers_created = 0
        careers_updated = 0
        
        for career_code, career_info in kb.careers_data.items():
            if force_update:
                career, created = Career.objects.update_or_create(
                    name=career_info['name'],
                    defaults={
                        'description': career_info['description'],
                        'category': career_info['category'],
                        'min_score_threshold': career_info['min_threshold'],
                        'growth_prospects': 'Good',
                        'salary_range': 'Competitive'
                    }
                )
                if created:
                    careers_created += 1
                else:
                    careers_updated += 1
            else:
                career, created = Career.objects.get_or_create(
                    name=career_info['name'],
                    defaults={
                        'description': career_info['description'],
                        'category': career_info['category'],
                        'min_score_threshold': career_info['min_threshold'],
                        'growth_prospects': 'Good',
                        'salary_range': 'Competitive'
                    }
                )
                if created:
                    careers_created += 1
            
            # Add required subjects
            if created or force_update:
                career.required_subjects.clear()  # Clear existing if force update
                for subject_code in career_info['required_subjects']:
                    subject_name = subject_code.replace('_', ' ').title()
                    try:
                        subject = Subject.objects.get(name=subject_name)
                        career.required_subjects.add(subject)
                    except Subject.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Subject "{subject_name}" not found for career "{career.name}"')
                        )
        
        self.stdout.write(f'Careers: {careers_created} created, {careers_updated} updated')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Data population complete! '
                f'Subjects: {subjects_created + subjects_updated}, '
                f'Careers: {careers_created + careers_updated}'
            )
        )
