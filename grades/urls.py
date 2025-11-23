from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('add-course/', views.add_course, name='add_course'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
