from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Enrollment
from .forms import CourseForm

# -------------------
# 學生功能
# -------------------
@login_required
def index(request):
    # 依登入帳號取得 Student
    student, _ = Student.objects.get_or_create(name=request.user.username)
    
    # 該學生的修課清單
    enrollments = Enrollment.objects.filter(student=student).select_related('course')

    # 可選課程：排除已選的
    courses = Course.objects.exclude(id__in=enrollments.values_list('course_id', flat=True))

    # 計算整體平均
    overall_avg = None
    if enrollments.exists():
        overall_avg = sum(e.average() for e in enrollments) / enrollments.count()

    return render(request, 'grades/index.html', {
        'student': student,
        'enrollments': enrollments,
        'courses': courses,
        'overall_avg': overall_avg,
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    return render(request, 'grades/course_detail.html', {'course': course, 'enrollments': enrollments})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CourseForm()
    return render(request, 'grades/add_course.html', {'form': form})

@login_required
def enroll_course(request, course_id):
    student = get_object_or_404(Student, name=request.user.username)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=student, course=course)
    return redirect('index')

@login_required
def unenroll_course(request, course_id):
    student = get_object_or_404(Student, name=request.user.username)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.filter(student=student, course=course).delete()
    return redirect('index')

# -------------------
# 登入/登出/註冊
# -------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'grades/login.html', {'error': '帳號或密碼錯誤'})
    return render(request, 'grades/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        # 自動建立對應 Student
        Student.objects.create(name=username)

        return redirect('login')
    return render(request, 'grades/register.html')
