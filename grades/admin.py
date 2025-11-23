from django.contrib import admin
from .models import Student, Course, Enrollment

# 讓 Student 在 Admin 顯示名字
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 列表顯示欄位
    search_fields = ('name',)  # 可搜尋學生名字

# 讓 Course 在 Admin 顯示課程名稱
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# 讓 Enrollment 在 Admin 顯示學生、課程，並可直接編輯分數
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'midterm_score', 'final_score', 'average_display')
    list_editable = ('midterm_score', 'final_score')  # 直接可編輯期中、期末分數
    search_fields = ('student__name', 'course__title')  # 搜尋學生或課程

    # 顯示平均分數
    def average_display(self, obj):
        return obj.average()
    average_display.short_description = '平均分數'
