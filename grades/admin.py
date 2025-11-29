from django.contrib import admin
from .models import Student, Teacher, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'user')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'teacher', 'teacher_fk')
    search_fields = ('title', 'code', 'teacher')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'midterm_score', 'final_score', 'average')
