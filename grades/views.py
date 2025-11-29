from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Student, Course, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Student, Teacher, Course, Enrollment
from .forms import EditProfileForm

def home_view(request):
    return render(request, 'grades/home.html')


def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and not user.is_staff:
            login(request, user)
            return redirect("grades:index")
        messages.error(request, "帳號或密碼錯誤，或非學生帳號")
    return render(request, "grades/student_login.html")


def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("grades:teacher_home")
        messages.error(request, "帳號或密碼錯誤，或非教師帳號")
    return render(request, "grades/teacher_login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(name=username, user=user)
        return redirect("grades:student_login")
    return render(request, "grades/register.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("grades:student_login")

@login_required
def teacher_stu_list(request):
    print("=== teacher_stu_list view 被呼叫 ===")

    # 1. 取得登入中的老師
    teacher = Teacher.objects.filter(user=request.user).first()
    print("登入老師：", teacher)

    if not teacher:
        print("沒有找到 teacher 資料")
        return render(request, 'grades/teacher_no_profile.html')

    # 2. 取得該老師所有課程（要用 teacher_fk）
    courses = Course.objects.filter(teacher_fk=teacher)
    print("老師的課程：", courses)

    # 3. 從 Enrollment 找出所有選修老師課程的學生
    enrollments = Enrollment.objects.filter(course__in=courses).select_related("student")
    students = [e.student for e in enrollments]
    print("找到的學生：", students)

    return render(request, 'grades/teacher_stu_list.html', {
        'students': students,
        'courses': courses,
    })


@login_required
def index(request):
    if request.user.is_staff:
        return redirect("grades:teacher_home")
    student, _ = Student.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
    enrollments = Enrollment.objects.filter(student=student).select_related("course")
    enrolled_ids = enrollments.values_list("course_id", flat=True)
    courses = Course.objects.exclude(id__in=enrolled_ids)
    overall_avg = round(sum(e.average() for e in enrollments)/enrollments.count(), 2) if enrollments.exists() else None
    return render(request, "grades/index.html", {
        "student": student,
        "enrollments": enrollments,
        "courses": courses,
        "overall_avg": overall_avg,
    })


@login_required
def enroll_course(request, course_id):
    student, _ = Student.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=student, course=course)
    return redirect("grades:index")


@login_required
def unenroll_course(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.filter(student=student, course=course).delete()
    return redirect("grades:index")


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related("student")
    return render(request, "grades/course_detail.html", {"course": course, "enrollments": enrollments})


@login_required
def edit_profile(request):
    student, _ = Student.objects.get_or_create(user=request.user, defaults={"name": request.user.username})
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("grades:index")
    else:
        form = EditProfileForm(instance=student)
    return render(request, "grades/edit_profile.html", {"form": form})


@login_required
def teacher_home(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        return render(request, "grades/teacher_no_profile.html")
    courses = Course.objects.filter(teacher_fk=teacher)
    return render(request, "grades/teacher_home.html", {"teacher": teacher, "courses": courses})


@login_required
def teacher_add_course(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        return redirect("grades:teacher_home")
    if request.method == "POST":
        title = request.POST.get("title")
        code = request.POST.get("code")
        Course.objects.create(title=title, code=code, teacher=teacher.name, teacher_fk=teacher)
        return redirect("grades:teacher_home")
    return render(request, "grades/teacher_add_course.html")

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('grades:teacher_home')

@login_required
def teacher_course_students(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher or course.teacher_fk != teacher:
        return render(request, "grades/permission_denied.html")
    enrollments = Enrollment.objects.filter(course=course).select_related("student")
    return render(request, "grades/teacher_course_students.html", {
        "course": course,
        "enrollments": enrollments
    })

@login_required
def teacher_edit_score(request, enroll_id):
    enroll = get_object_or_404(Enrollment, id=enroll_id)
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher or enroll.course.teacher_fk != teacher:
        return render(request, "grades/permission_denied.html")
    if request.method == "POST":
        enroll.midterm_score = request.POST.get("midterm_score") or 0
        enroll.final_score = request.POST.get("final_score") or 0
        enroll.save()
        return redirect("grades:teacher_course_students", course_id=enroll.course.id)
    return render(request, "grades/teacher_edit_score.html", {"enroll": enroll})

@login_required
def student_list(request):
    # 取得老師自己課程
    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        students = Student.objects.none()
    else:
        courses = Course.objects.filter(teacher_fk=teacher)
        # 抓選了老師課程的學生
        students = Student.objects.filter(enrollment__course__in=courses).distinct()
        # 把學生跟課程關聯抓進來
        students = students.prefetch_related('enrollment_set__course')
    
    return render(request, "grades/student_list.html", {"students": students, "teacher": teacher})

