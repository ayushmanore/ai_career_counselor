from django.db import models
from django.contrib.auth.models import User
import json
from datetime import datetime

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    weight = models.FloatField(default=1.0)
    
    def __str__(self):
        return self.name

class Career(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    required_subjects = models.ManyToManyField(Subject, blank=True)
    min_score_threshold = models.FloatField(default=60.0)
    growth_prospects = models.CharField(max_length=50, default='Good')
    salary_range = models.CharField(max_length=100, default='Competitive')
    
    def __str__(self):
        return self.name

class StudentAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    education_level = models.CharField(max_length=50)
    subject_scores = models.JSONField()  # Store subject preferences and scores
    personality_traits = models.JSONField(default=dict)
    career_interests = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.session_id}"

class CareerRecommendation(models.Model):
    assessment = models.ForeignKey(StudentAssessment, on_delete=models.CASCADE, related_name='recommendations')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, null=True, blank=True)
    confidence_score = models.FloatField()
    reasoning = models.TextField()
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Allow null for existing rows

    class Meta:
        ordering = ['rank']
        unique_together = ['assessment', 'career']

    def __str__(self):
        career_name = self.career.name if self.career else "Unknown Career"
        return f"{career_name} - {self.confidence_score}%"

    @property
    def confidence_percent(self):
        """Convert confidence_score into a clean 0-100 percentage"""
        if self.confidence_score is None:
            return 0
        if 0 <= self.confidence_score <= 1:  # normalized (0-1)
            return round(self.confidence_score * 100)
        return round(self.confidence_score)  # already in %
    
    @property
    def match_level(self):
        """Return match quality as text"""
        score = self.confidence_percent
        if score >= 80:
            return "Excellent Match"
        elif score >= 60:
            return "Good Match"
        elif score >= 40:
            return "Fair Match"
        else:
            return "Low Match"
    
    @property
    def confidence_class(self):
        """Return CSS class based on confidence level"""
        score = self.confidence_percent
        if score >= 80:
            return "confidence-high"
        elif score >= 60:
            return "confidence-medium"
        else:
            return "confidence-low"