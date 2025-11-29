from django import forms
from .models import Course, Student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'teacher']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['display_name', 'avatar']
