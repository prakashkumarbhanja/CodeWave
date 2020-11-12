from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import User

class Student(models.Model):
  user_std = models.OneToOneField(User,
          on_delete = models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.user_std.username

class Teacher(models.Model):
  user_tchr = models.OneToOneField(User,
          on_delete = models.CASCADE, null=True, blank=True)

  def __str__(self):
    return self.user_tchr.username

class classrooms(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)
    course_img = models.ImageField(upload_to='course_img/',null=True, blank=True)
    description = models.CharField(max_length=220)
    add_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return "{} by {}".format(self.course_name, self.teacher.user_tchr.username)

    @property
    def image_url(self):
        return self.course_img.url


class Enroll_Courses(models.Model):
    enrolled_class = models.ForeignKey(classrooms, on_delete=models.CASCADE)
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return self.enrolled_class.course_name