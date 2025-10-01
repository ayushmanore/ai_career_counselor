from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('assessment/', views.assessment_view, name='assessment_form'),  # single route for form
    path('results/<uuid:session_id>/', views.results, name='results'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/career-suggestions/', views.api_career_suggestions, name='api_career_suggestions'),
]
