from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# allows creation of different users
# class User(AbstractUser):
#     class Role(models.TextChoices):
#         TUTOR = "tutor"
#         STUDENT = "student"


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


# tutor model, only holds username for now
class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField()  # can add computing id


# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField()  # can add computing id
