from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField('課名', max_length=200)
    code = models.CharField('課號', max_length=20)
    teacher = models.CharField('任課老師', max_length=100)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_score = models.FloatField(default=0)
    final_score = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'course')

    def average(self):
        mid = self.midterm_score or 0
        fin = self.final_score or 0
        return round((mid + fin) / 2, 2)

    def __str__(self):
        return f"{self.student} - {self.course}"
