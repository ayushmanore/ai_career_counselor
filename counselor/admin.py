from django.contrib import admin
from .models import Subject, Career, StudentAssessment, CareerRecommendation

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'weight']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['category', 'name']

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'min_score_threshold', 'growth_prospects']
    list_filter = ['category', 'growth_prospects']
    search_fields = ['name', 'description']
    filter_horizontal = ['required_subjects']
    ordering = ['category', 'name']

@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'education_level', 'created_at', 'session_id']
    list_filter = ['education_level', 'created_at']
    search_fields = ['name', 'session_id']
    readonly_fields = ['session_id', 'created_at']
    ordering = ['-created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['session_id', 'created_at', 'subject_scores', 'personality_traits']
        return ['session_id', 'created_at']

@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'get_career_name', 'confidence_score', 'rank']
    list_filter = ['rank']
    search_fields = ['assessment__name', 'reasoning']
    ordering = ['assessment', 'rank']
    
    def get_career_name(self, obj):
        return obj.career.name if obj.career else "Custom Career"
    get_career_name.short_description = 'Career'