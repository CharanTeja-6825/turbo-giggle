from django import forms
from django.contrib.auth.models import User

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'duration', 'serial_number', 'description', 'trainer']

        widgets = {
            'course_name': forms.TextInput(attrs={'placeholder': 'Enter course name'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Enter duration'}),
            'serial_number': forms.TextInput(attrs={'placeholder': 'Enter serial number'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter course description'}),
            'trainer': forms.Select(attrs={'placeholder': 'Select a trainer'}),
        }

from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'file', 'course']

    # file = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #     required=False  # Optional, depending on your needs
    # )
# forms.py
from django import forms
from .models import TrainingInquiry

class TrainingInquiryForm(forms.ModelForm):
    class Meta:
        model = TrainingInquiry
        fields = ['full_name', 'email', 'mobile', 'company_name', 'participants', 'message']


from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['trainer', 'rating', 'comments']

    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    trainer = forms.ModelChoiceField(queryset=User.objects.filter(username__regex=r'^\d{4}$'),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
