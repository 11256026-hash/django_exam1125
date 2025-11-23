# grades/forms.py
from django import forms
from .models import Course, Enrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'teacher']


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'midterm_score', 'final_score']