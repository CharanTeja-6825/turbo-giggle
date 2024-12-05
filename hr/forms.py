from django import forms
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
