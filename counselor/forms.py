from django import forms

SUBJECT_CHOICES = [
    ('mathematics', 'Mathematics'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('biology', 'Biology'),
    ('computer_science', 'Computer Science'),
    ('english', 'English'),
    ('history', 'History'),
    ('geography', 'Geography'),
    ('economics', 'Economics'),
    ('business_studies', 'Business Studies'),
    ('art', 'Art'),
    ('music', 'Music'),
    ('physical_education', 'Physical Education'),
]

EDUCATION_LEVEL_CHOICES = [
    ('high_school', 'High School'),
    ('undergraduate', 'Undergraduate'),
    ('graduate', 'Graduate'),
]

class StudentAssessmentForm(forms.Form):
    # Basic Information
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your full name'
    }))
    
    age = forms.IntegerField(min_value=13, max_value=50, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your age'
    }))
    
    education_level = forms.ChoiceField(choices=EDUCATION_LEVEL_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    # Subject Scores (0-100)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically add subject score fields
        for subject_code, subject_name in SUBJECT_CHOICES:
            self.fields[f'score_{subject_code}'] = forms.IntegerField(
                label=f'{subject_name} Score (0-100)',
                min_value=0,
                max_value=100,
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': f'Enter your {subject_name} score'
                })
            )
    
    # Career Interests
    career_interests = forms.MultipleChoiceField(
        choices=[
            ('technology', 'Technology'),
            ('healthcare', 'Healthcare'),
            ('business', 'Business'),
            ('education', 'Education'),
            ('creative', 'Creative Arts'),
            ('science', 'Science & Research'),
            ('engineering', 'Engineering'),
            ('finance', 'Finance'),
            ('media', 'Media & Communication'),
            ('social_work', 'Social Work'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    # Personality Questions
    enjoys_problem_solving = forms.BooleanField(
        label="I enjoy solving complex problems",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    prefers_working_with_people = forms.BooleanField(
        label="I prefer working with people over working alone",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    enjoys_creative_activities = forms.BooleanField(
        label="I enjoy creative and artistic activities",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    likes_leadership_roles = forms.BooleanField(
        label="I like taking leadership roles",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    interested_in_helping_others = forms.BooleanField(
        label="I am interested in helping others",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    enjoys_analytical_thinking = forms.BooleanField(
        label="I enjoy analytical and logical thinking",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
