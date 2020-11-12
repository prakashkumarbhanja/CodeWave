from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from enrollment.models import (Student, Teacher)

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user_std=instance)