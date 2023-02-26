from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# allows creation of different users
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        TUTOR = "TUTOR", 'Tutor'
        STUDENT = "STUDENT", 'Student'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save()

# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)


# tutor model, only holds username for now
# class Tutor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.TextField()  # can add computing id


# Student model
# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.TextField()  # can add computing id
