from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    classes = models.TextField(max_length=1000, default="")


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=200)
    year = models.TextField(max_length=500)
    classes = models.TextField(max_length=1000, default="")


#   verify_student = models.BooleanField(default=False)
#   verify_tutor = models.BooleanField(default=False)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=200)
    year = models.TextField(max_length=500)
    classes = models.TextField(max_length=1000, default="")


#   verify_student = models.BooleanField(default=False)
#   verify_tutor = models.BooleanField(default=False)

class TutorClasses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classlist", null=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class StudentClasses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="class_list", null=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name



class Classes(models.Model):
    tutorclass = models.ForeignKey(TutorClasses, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
