from django.urls import path
from . import views

app_name = "grades"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/teacher/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('grades/teacher/', views.teacher_home, name='teacher_home'),


    path('dashboard/', views.index, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    path('teacher/course/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/add_course/', views.teacher_add_course, name='teacher_add_course'),
    path('teacher/course/<int:course_id>/students/', views.teacher_course_students, name='teacher_course_students'),
    path('teacher/enrollment/<int:enroll_id>/edit/', views.teacher_edit_score, name='teacher_edit_score'),
    path('teacher/students/', views.student_list, name='student_list'),
    path('teacher/students/', views.teacher_stu_list, name='teacher_stu_list'),

    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/add_message/', views.add_message, name='add_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),

]

