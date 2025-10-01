from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
import uuid
from .forms import StudentAssessmentForm, SUBJECT_CHOICES
from .models import StudentAssessment, CareerRecommendation, Career
from .auth_forms import CustomUserCreationForm, LoginForm
from .models import StudentAssessment, CareerRecommendation, Career

# Import AI engines with error handling
try:
    from .ai_engine.knowledge_base import KnowledgeBase
    from .ai_engine.fopl_rules import FOPLRuleEngine
    from .ai_engine.inference_engine import ForwardChainingEngine
    from .ai_engine.uncertainty_engine import UncertaintyEngine
    AI_ENGINES_AVAILABLE = True
except ImportError:
    AI_ENGINES_AVAILABLE = False
    print("Warning: AI engines not found. Using fallback career inference.")

def home(request):
    """Home page view"""
    return render(request, 'counselor/home.html')

def about(request):
    """About page explaining the AI system"""
    return render(request, 'counselor/about.html')

# Add this updated assessment function to your views.py

def assessment(request):
    """Enhanced assessment form view with AI integration"""
    if request.method == 'POST':
        try:
            # Get basic form data
            name = request.POST.get('name')
            age = request.POST.get('age')
            education_level = request.POST.get('education_level')
            interests = request.POST.getlist('interests')
            
            # Get subject scores
            subject_scores = {}
            subject_fields = [
                'mathematics', 'physics', 'chemistry', 'biology', 'computer_science',
                'english', 'history', 'economics', 'business_studies', 'art'
            ]
            
            for subject in subject_fields:
                score = request.POST.get(f'score_{subject}')
                if score and score.strip():  # Only add if score is provided
                    try:
                        subject_scores[subject] = int(score)
                    except ValueError:
                        pass  # Skip invalid scores
            
            # Get personality traits
            personality_traits = {
                'problem_solving': request.POST.get('enjoys_problem_solving') == 'on',
                'social': request.POST.get('prefers_working_with_people') == 'on',
                'creative': request.POST.get('enjoys_creative_activities') == 'on',
                'leadership': request.POST.get('likes_leadership_roles') == 'on',
                'helping': request.POST.get('interested_in_helping_others') == 'on',
                'analytical': request.POST.get('enjoys_analytical_thinking') == 'on',
            }
            
            print(f"Collected data: name={name}, age={age}, education={education_level}")
            print(f"Subject scores: {subject_scores}")
            print(f"Interests: {interests}")
            print(f"Personality: {personality_traits}")
            
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            # Create assessment
            assessment_obj = StudentAssessment.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                name=name,
                age=int(age),
                education_level=education_level,
                subject_scores=subject_scores,
                personality_traits=personality_traits,
                career_interests=interests
            )
            
            print(f"Created assessment: {assessment_obj.id}")
            
            # Run AI inference - choose method based on available data
            if subject_scores:
                print("Using AI engines (subject scores available)")
                recommendations = run_advanced_ai_inference(assessment_obj)
            else:
                print("Using fallback inference (no subject scores)")
                recommendations = run_career_inference(assessment_obj)
            
            print(f"Generated {len(recommendations)} recommendations")
            
            # Save recommendations
            save_recommendations(assessment_obj, recommendations)
            
            # Redirect to results
            return redirect('results', session_id=session_id)
            
        except Exception as e:
            print(f"Error in assessment view: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f"There was an error processing your assessment: {str(e)}")
            return render(request, 'counselor/assessment_form.html')
    
    # GET request - show form
    return render(request, 'counselor/assessment_form.html')

def run_advanced_ai_inference(assessment):
    """Run the advanced AI inference using FOPL engines"""
    student_data = {
        'subject_scores': assessment.subject_scores,
        'personality_traits': assessment.personality_traits,
        'career_interests': assessment.career_interests,
        'age': assessment.age,
        'education_level': assessment.education_level
    }
    
    print(f"Running advanced AI inference with data: {student_data}")
    
    if AI_ENGINES_AVAILABLE:
        try:
            # Initialize AI components
            kb = KnowledgeBase()
            fopl_engine = FOPLRuleEngine(kb)
            inference_engine = ForwardChainingEngine(kb, fopl_engine)
            uncertainty_engine = UncertaintyEngine()
            
            print("AI engines initialized successfully")
            
            # Run inference
            recommendations = inference_engine.infer_careers(student_data)
            print(f"Inference engine returned {len(recommendations)} recommendations")
            
            # Apply uncertainty if available
            try:
                adjusted_recommendations = uncertainty_engine.apply_uncertainty_to_recommendations(recommendations)
                print(f"Uncertainty engine adjusted to {len(adjusted_recommendations)} recommendations")
                return adjusted_recommendations
            except Exception as e:
                print(f"Uncertainty engine error: {e}, using raw recommendations")
                return recommendations
                
        except Exception as e:
            print(f"AI Engine error: {e}")
            import traceback
            traceback.print_exc()
            return fallback_career_inference(student_data)
    else:
        print("AI engines not available, using fallback")
        return fallback_career_inference(student_data)

def enhanced_fallback_career_inference(student_data):
    """Enhanced fallback that can use subject scores if available"""
    recommendations = []
    
    subject_scores = student_data.get('subject_scores', {})
    interests = student_data.get('career_interests', [])
    personality = student_data.get('personality_traits', {})
    education_level = student_data.get('education_level', 'highschool')
    
    print(f"Enhanced fallback - Subject scores: {len(subject_scores)}, Interests: {interests}")
    
    # If we have subject scores, use them for more accurate recommendations
    if subject_scores:
        # Technology careers based on subject performance
        if (subject_scores.get('mathematics', 0) >= 75 and 
            subject_scores.get('computer_science', 0) >= 75):
            recommendations.append({
                'career_name': 'Software Engineer',
                'confidence_score': 90,
                'reasoning': f"Excellent in Mathematics ({subject_scores.get('mathematics', 0)}%) and Computer Science ({subject_scores.get('computer_science', 0)}%)",
                'category': 'Technology',
                'description': 'Design and develop software applications',
                'salary_range': '$70,000 - $120,000',
                'growth_prospects': 'High'
            })
        
        # Medical careers
        if (subject_scores.get('biology', 0) >= 80 and 
            subject_scores.get('chemistry', 0) >= 80 and
            subject_scores.get('physics', 0) >= 70):
            recommendations.append({
                'career_name': 'Medical Doctor',
                'confidence_score': 92,
                'reasoning': f"Outstanding performance in Biology ({subject_scores.get('biology', 0)}%), Chemistry ({subject_scores.get('chemistry', 0)}%), and Physics ({subject_scores.get('physics', 0)}%)",
                'category': 'Healthcare',
                'description': 'Diagnose and treat patients',
                'salary_range': '$150,000 - $300,000',
                'growth_prospects': 'High'
            })
        
        # Engineering careers
        if (subject_scores.get('mathematics', 0) >= 75 and 
            subject_scores.get('physics', 0) >= 75):
            recommendations.append({
                'career_name': 'Mechanical Engineer',
                'confidence_score': 88,
                'reasoning': f"Strong foundation in Mathematics ({subject_scores.get('mathematics', 0)}%) and Physics ({subject_scores.get('physics', 0)}%)",
                'category': 'Engineering',
                'description': 'Design and build mechanical systems',
                'salary_range': '$70,000 - $115,000',
                'growth_prospects': 'High'
            })
        
        # Business/Finance careers
        if (subject_scores.get('mathematics', 0) >= 70 and 
            subject_scores.get('economics', 0) >= 70):
            recommendations.append({
                'career_name': 'Financial Analyst',
                'confidence_score': 85,
                'reasoning': f"Good analytical skills shown in Mathematics ({subject_scores.get('mathematics', 0)}%) and Economics ({subject_scores.get('economics', 0)}%)",
                'category': 'Finance',
                'description': 'Analyze financial data and investments',
                'salary_range': '$60,000 - $95,000',
                'growth_prospects': 'Medium'
            })
        
        # Creative careers
        if subject_scores.get('art', 0) >= 70:
            recommendations.append({
                'career_name': 'Graphic Designer',
                'confidence_score': 82,
                'reasoning': f"Creative talent demonstrated in Art ({subject_scores.get('art', 0)}%)",
                'category': 'Creative',
                'description': 'Create visual designs and artwork',
                'salary_range': '$40,000 - $70,000',
                'growth_prospects': 'Medium'
            })
        
        # Education careers
        if subject_scores.get('english', 0) >= 75:
            recommendations.append({
                'career_name': 'Teacher',
                'confidence_score': 80,
                'reasoning': f"Strong communication skills shown in English ({subject_scores.get('english', 0)}%)",
                'category': 'Education',
                'description': 'Educate and inspire students',
                'salary_range': '$40,000 - $65,000',
                'growth_prospects': 'Medium'
            })
    
    # If no recommendations from subject scores, fall back to interest-based recommendations
    if not recommendations:
        recommendations = fallback_career_inference(student_data)
    
    # Sort by confidence score
    recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
    
    return recommendations[:8]
def results(request, session_id):
    """Display career recommendations"""
    try:
        assessment = StudentAssessment.objects.get(session_id=session_id)
        recommendations = CareerRecommendation.objects.filter(assessment=assessment).order_by('rank')
        
        print(f"Found assessment: {assessment.name}, {len(recommendations)} recommendations")
        
        context = {
            'assessment': assessment,
            'recommendations': recommendations,
            'session_id': session_id,
            'interests': assessment.career_interests if assessment.career_interests else []
        }
        
        return render(request, 'counselor/results.html', context)
    
    except StudentAssessment.DoesNotExist:
        print(f"Assessment not found for session_id: {session_id}")
        messages.error(request, "Assessment not found.")
        return redirect('assessment')

@csrf_exempt
def api_career_suggestions(request):
    """API endpoint for getting career suggestions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create temporary assessment data
            student_data = {
                'subject_scores': data.get('subject_scores', {}),
                'personality_traits': data.get('personality_traits', {}),
                'career_interests': data.get('career_interests', [])
            }
            
            # Run inference
            if AI_ENGINES_AVAILABLE:
                try:
                    kb = KnowledgeBase()
                    fopl_engine = FOPLRuleEngine(kb)
                    inference_engine = ForwardChainingEngine(kb, fopl_engine)
                    uncertainty_engine = UncertaintyEngine()
                    
                    recommendations = inference_engine.infer_careers(student_data)
                    adjusted_recommendations = uncertainty_engine.apply_uncertainty_to_recommendations(recommendations)
                except Exception as e:
                    print(f"AI Engine error: {e}")
                    adjusted_recommendations = fallback_career_inference(student_data)
            else:
                adjusted_recommendations = fallback_career_inference(student_data)
            
            return JsonResponse({
                'success': True,
                'recommendations': adjusted_recommendations[:5]  # Top 5
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def run_career_inference(assessment):
    """Run the AI career inference system"""
    # Prepare student data
    student_data = {
        'subject_scores': assessment.subject_scores,
        'personality_traits': assessment.personality_traits,
        'career_interests': assessment.career_interests,
        'age': assessment.age,
        'education_level': assessment.education_level
    }
    
    print(f"Running inference with data: {student_data}")
    
    if AI_ENGINES_AVAILABLE:
        try:
            # Initialize AI components
            kb = KnowledgeBase()
            fopl_engine = FOPLRuleEngine(kb)
            inference_engine = ForwardChainingEngine(kb, fopl_engine)
            uncertainty_engine = UncertaintyEngine()
            
            # Run inference
            recommendations = inference_engine.infer_careers(student_data)
            adjusted_recommendations = uncertainty_engine.apply_uncertainty_to_recommendations(recommendations)
            
            return adjusted_recommendations
        except Exception as e:
            print(f"AI Engine error: {e}")
            return fallback_career_inference(student_data)
    else:
        print("Using fallback inference")
        return fallback_career_inference(student_data)

def enhanced_fallback_career_inference(student_data):
    """Enhanced fallback with DYNAMIC scoring based on actual performance"""
    recommendations = []
    
    subject_scores = student_data.get('subject_scores', {})
    interests = student_data.get('career_interests', [])
    personality = student_data.get('personality_traits', {})
    education_level = student_data.get('education_level', 'highschool')
    
    print(f"Enhanced fallback - Subject scores: {subject_scores}")
    
    if subject_scores:
        # SOFTWARE ENGINEERING - Calculate average of relevant subjects
        math = subject_scores.get('mathematics', 0)
        cs = subject_scores.get('computer_science', 0)
        
        if math >= 60 and cs >= 60:
            # Base score is average of the two subjects
            base_score = (math + cs) / 2
            
            # Small personality bonuses (max +8)
            if personality.get('analytical', False):
                base_score += 3
            if personality.get('problem_solving', False):
                base_score += 3
            if personality.get('creative', False):
                base_score += 2
            
            # Cap at 95
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Software Engineer',
                'confidence_score': final_score,
                'reasoning': f"Strong in Mathematics ({math}%) and Computer Science ({cs}%)",
                'category': 'Technology',
                'description': 'Design and develop software applications',
                'salary_range': '$70,000 - $120,000',
                'growth_prospects': 'High'
            })
        
        # MEDICAL DOCTOR - Average of bio, chem, physics
        bio = subject_scores.get('biology', 0)
        chem = subject_scores.get('chemistry', 0)
        phys = subject_scores.get('physics', 0)
        
        if bio >= 65 and chem >= 65 and phys >= 60:
            base_score = (bio + chem + phys) / 3
            
            if personality.get('helping', False):
                base_score += 4
            if personality.get('analytical', False):
                base_score += 3
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Medical Doctor',
                'confidence_score': final_score,
                'reasoning': f"Strong performance in Biology ({bio}%), Chemistry ({chem}%), Physics ({phys}%)",
                'category': 'Healthcare',
                'description': 'Diagnose and treat patients',
                'salary_range': '$150,000 - $300,000',
                'growth_prospects': 'High'
            })
        
        # MECHANICAL ENGINEER - Math + Physics average
        if math >= 60 and phys >= 60:
            base_score = (math + phys) / 2
            
            if personality.get('problem_solving', False):
                base_score += 3
            if personality.get('analytical', False):
                base_score += 2
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Mechanical Engineer',
                'confidence_score': final_score,
                'reasoning': f"Solid foundation in Mathematics ({math}%) and Physics ({phys}%)",
                'category': 'Engineering',
                'description': 'Design and build mechanical systems',
                'salary_range': '$70,000 - $115,000',
                'growth_prospects': 'High'
            })
        
        # FINANCIAL ANALYST - Math + Economics
        econ = subject_scores.get('economics', 0)
        
        if math >= 60 and econ >= 60:
            base_score = (math + econ) / 2
            
            if personality.get('analytical', False):
                base_score += 3
            if personality.get('leadership', False):
                base_score += 2
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Financial Analyst',
                'confidence_score': final_score,
                'reasoning': f"Good analytical skills in Mathematics ({math}%) and Economics ({econ}%)",
                'category': 'Finance',
                'description': 'Analyze financial data and investments',
                'salary_range': '$60,000 - $95,000',
                'growth_prospects': 'Medium'
            })
        
        # GRAPHIC DESIGNER - Art score
        art = subject_scores.get('art', 0)
        
        if art >= 55:
            base_score = art
            
            if personality.get('creative', False):
                base_score += 5
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Graphic Designer',
                'confidence_score': final_score,
                'reasoning': f"Creative talent in Art ({art}%)",
                'category': 'Creative',
                'description': 'Create visual designs and artwork',
                'salary_range': '$40,000 - $70,000',
                'growth_prospects': 'Medium'
            })
        
        # DATA SCIENTIST - Math + CS + some stat thinking
        if math >= 70 and cs >= 65:
            base_score = (math + cs) / 2
            
            if personality.get('analytical', False):
                base_score += 4
            if personality.get('problem_solving', False):
                base_score += 3
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Data Scientist',
                'confidence_score': final_score,
                'reasoning': f"Strong analytical skills in Mathematics ({math}%) and Computer Science ({cs}%)",
                'category': 'Technology',
                'description': 'Analyze complex data to help organizations make decisions',
                'salary_range': '$80,000 - $140,000',
                'growth_prospects': 'High'
            })
        
        # TEACHER - English or best subject score
        english = subject_scores.get('english', 0)
        
        if english >= 60:
            base_score = english
            
            if personality.get('helping', False):
                base_score += 4
            if personality.get('social', False):
                base_score += 3
            
            final_score = min(int(base_score), 95)
            
            recommendations.append({
                'career_name': 'Teacher',
                'confidence_score': final_score,
                'reasoning': f"Strong communication skills in English ({english}%)",
                'category': 'Education',
                'description': 'Educate and inspire students',
                'salary_range': '$40,000 - $65,000',
                'growth_prospects': 'Medium'
            })
    
    # If no recommendations from subject scores, use fallback
    if not recommendations:
        recommendations = fallback_career_inference(student_data)
    
    # Sort by confidence score and return top 8
    recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
    return recommendations[:8]


def fallback_career_inference(student_data):
    """Fallback with REALISTIC base scores (50-75 range)"""
    recommendations = []
    
    subject_scores = student_data.get('subject_scores', {})
    interests = student_data.get('career_interests', [])
    personality = student_data.get('personality_traits', {})
    education_level = student_data.get('education_level', 'highschool')
    age = student_data.get('age', 18)
    
    # REALISTIC base scores based on education level
    career_mappings = {
        'engineering': {
            'highschool': [
                ('Software Developer Trainee', 55, 'Entry-level programming'),
                ('Engineering Technician', 52, 'Technical support role'),
                ('CAD Drafter', 54, 'Technical drawing'),
                ('IT Support Specialist', 50, 'Computer support')
            ],
            'undergrad': [
                ('Software Engineer', 68, 'Full-stack development'),
                ('Mechanical Engineer', 66, 'Design and manufacturing'),
                ('Civil Engineer', 65, 'Infrastructure projects'),
                ('Electrical Engineer', 67, 'Electronics systems'),
                ('Data Engineer', 64, 'Big data infrastructure')
            ],
            'postgrad': [
                ('Senior Software Architect', 75, 'Advanced system design'),
                ('Research Engineer', 73, 'Technology research'),
                ('Engineering Manager', 72, 'Technical leadership'),
                ('AI/ML Engineer', 74, 'Machine learning'),
                ('Principal Engineer', 71, 'Technical strategy')
            ]
        },
        'science': {
            'highschool': [
                ('Lab Technician', 52, 'Laboratory support'),
                ('Medical Assistant', 54, 'Healthcare support'),
                ('Science Teacher Assistant', 50, 'Educational support'),
            ],
            'undergrad': [
                ('Research Scientist', 66, 'Scientific research'),
                ('Data Analyst', 64, 'Statistical analysis'),
                ('Environmental Scientist', 63, 'Environmental protection'),
                ('Biologist', 65, 'Life sciences research'),
            ],
            'postgrad': [
                ('Senior Research Scientist', 73, 'Research leadership'),
                ('Principal Investigator', 75, 'Grant-funded research'),
                ('Science Director', 72, 'Science management'),
                ('Medical Researcher', 74, 'Biomedical research'),
            ]
        },
        'business': {
            'highschool': [
                ('Sales Representative', 48, 'Product sales'),
                ('Customer Service Manager', 50, 'Customer support'),
                ('Office Manager', 52, 'Administrative support'),
            ],
            'undergrad': [
                ('Business Analyst', 62, 'Business process analysis'),
                ('Marketing Manager', 64, 'Brand management'),
                ('Financial Advisor', 63, 'Financial planning'),
                ('Project Manager', 66, 'Project coordination'),
            ],
            'postgrad': [
                ('Business Consultant', 70, 'Strategic advisory'),
                ('Strategy Director', 73, 'Corporate strategy'),
                ('Investment Manager', 72, 'Portfolio management'),
                ('Management Consultant', 71, 'Organizational transformation'),
            ]
        },
        'arts': {
            'highschool': [
                ('Graphic Design Assistant', 50, 'Visual design support'),
                ('Creative Assistant', 52, 'Creative projects'),
                ('Social Media Creator', 54, 'Content creation'),
            ],
            'undergrad': [
                ('UX/UI Designer', 66, 'User experience design'),
                ('Art Director', 64, 'Creative direction'),
                ('Creative Writer', 62, 'Content writing'),
                ('Brand Designer', 63, 'Brand identity'),
            ],
            'postgrad': [
                ('Creative Director', 72, 'Creative leadership'),
                ('Art Gallery Owner', 70, 'Art business'),
                ('Professor of Arts', 69, 'Arts education'),
                ('Design Strategist', 73, 'Design thinking'),
            ]
        }
    }
    
    # Generate recommendations
    for interest in interests:
        if interest in career_mappings:
            careers = career_mappings[interest].get(education_level, [])
            for career_title, base_score, description in careers:
                adjusted_score = base_score
                
                # Personality adjustments (max +10 total)
                if interest == 'engineering':
                    if personality.get('analytical', False):
                        adjusted_score += 4
                    if personality.get('problem_solving', False):
                        adjusted_score += 4
                elif interest == 'science':
                    if personality.get('analytical', False):
                        adjusted_score += 3
                    if personality.get('helping', False):
                        adjusted_score += 3
                elif interest == 'business':
                    if personality.get('leadership', False):
                        adjusted_score += 4
                    if personality.get('social', False):
                        adjusted_score += 3
                elif interest == 'arts':
                    if personality.get('creative', False):
                        adjusted_score += 5
                
                # Small age bonus
                if age < 25 and interest in ['engineering', 'science']:
                    adjusted_score += 2
                
                # Cap at 85 for interest-only matches
                adjusted_score = min(adjusted_score, 85)
                
                recommendations.append({
                    'career_name': career_title,
                    'confidence_score': int(adjusted_score),
                    'reasoning': f"{description}. Matches {interest} interest and {education_level} level.",
                    'category': interest.title(),
                    'description': description,
                    'salary_range': get_salary_range(career_title),
                    'growth_prospects': 'High' if adjusted_score > 70 else 'Medium'
                })
    
    # General recommendations if no interests
    if not recommendations:
        general = {
            'highschool': [('Customer Service Representative', 45), ('Administrative Assistant', 47)],
            'undergrad': [('Business Analyst', 58), ('Project Coordinator', 60)],
            'postgrad': [('Management Consultant', 68), ('Research Analyst', 66)]
        }
        
        for career_title, score in general.get(education_level, general['undergrad']):
            recommendations.append({
                'career_name': career_title,
                'confidence_score': score,
                'reasoning': f"General match for {education_level} education",
                'category': 'General',
                'description': 'Professional career path',
                'salary_range': get_salary_range(career_title),
                'growth_prospects': 'Medium'
            })
    
    # Remove duplicates
    seen = set()
    unique = []
    for rec in recommendations:
        if rec['career_name'] not in seen:
            seen.add(rec['career_name'])
            unique.append(rec)
    
    unique.sort(key=lambda x: x['confidence_score'], reverse=True)
    return unique[:8]

def get_salary_range(career_title):
    """Get salary range for a career"""
    salary_ranges = {
        # Technology
        'Software Engineer': '$70,000 - $120,000',
        'Software Developer Trainee': '$40,000 - $60,000',
        'Data Engineer': '$75,000 - $130,000',
        'AI/ML Engineer': '$90,000 - $160,000',
        'Senior Software Architect': '$120,000 - $200,000',
        'IT Support Specialist': '$35,000 - $55,000',
        
        # Business
        'Business Analyst': '$60,000 - $95,000',
        'Marketing Manager': '$65,000 - $110,000',
        'Project Manager': '$70,000 - $120,000',
        'Financial Advisor': '$55,000 - $95,000',
        'Business Consultant': '$80,000 - $150,000',
        'CEO/Executive': '$150,000 - $500,000+',
        
        # Science
        'Research Scientist': '$65,000 - $110,000',
        'Data Analyst': '$50,000 - $85,000',
        'Lab Technician': '$35,000 - $55,000',
        'Environmental Scientist': '$55,000 - $90,000',
        
        # Arts & Design
        'UX/UI Designer': '$55,000 - $90,000',
        'Graphic Design Assistant': '$30,000 - $45,000',
        'Art Director': '$65,000 - $110,000',
        'Creative Director': '$90,000 - $150,000',
        
        # Engineering
        'Mechanical Engineer': '$70,000 - $115,000',
        'Civil Engineer': '$65,000 - $105,000',
        'Electrical Engineer': '$70,000 - $120,000',
        'Engineering Technician': '$45,000 - $70,000',
    }
    return salary_ranges.get(career_title, '$40,000 - $80,000')

def save_recommendations(assessment, recommendations):
    """Save recommendations to database"""
    print(f"Saving {len(recommendations)} recommendations for assessment {assessment.id}")

    for i, rec in enumerate(recommendations):
        # Create or get Career object
        career, created = Career.objects.get_or_create(
            name=rec.get('career_name', 'Unknown Career'),
            defaults={
                'category': rec.get('category', 'General'),
                'description': rec.get('description', rec.get('reasoning', 'No description provided'))
            }
        )

        # Create the recommendation linked to the career
        CareerRecommendation.objects.create(
            assessment=assessment,
            career=career,
            confidence_score=rec.get('confidence_score', 0),
            reasoning=rec.get('reasoning', 'No reasoning provided'),
            rank=i + 1
        )

    print(f"Successfully saved {len(recommendations)} recommendations")

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'counselor/login.html', {'form': form})

def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to AI Career Counselor, {user.first_name or user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'counselor/register.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard showing their assessments"""
    assessments = StudentAssessment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'counselor/dashboard.html', {'assessments': assessments})
def assessment_view(request):
    """Alias for the main assessment function"""
    return assessment(request)
# Remove the duplicate assessment_view function - use the main assessment function instead