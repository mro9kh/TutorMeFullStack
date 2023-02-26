from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.TextField(max_length=200)
    name = models.TextField(max_length=200)
    year = models.TextField(max_length = 500)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.TextField(max_length=200)
    name = models.TextField(max_length=200)
    year = models.TextField(max_length=500)
