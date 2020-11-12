from django.contrib import admin
from enrollment.models import (Student, Teacher, classrooms, Enroll_Courses)

admin.site.register(Student)
admin.site.register(Teacher)

class classroomsAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course_name', 'add_on')
admin.site.register(classrooms, classroomsAdmin)
admin.site.register(Enroll_Courses)
