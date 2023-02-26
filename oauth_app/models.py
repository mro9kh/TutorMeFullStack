from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# allows creation of different users
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        TUTOR = "TUTOR", 'Tutor'
        STUDENT = "STUDENT", 'Student'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save()


# Tutor model
class Tutor(User):
    base_role = User.Role.TUTOR

    class Meta:
        proxy = True


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computing_id = models.CharField(max_length=50)


@receiver(post_save, sender=Tutor)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TUTOR":
        TutorProfile.objects.create(user=instance)


# ***********************************************************************************************************************
# Student model
class Student(User):
    base_role = User.Role.STUDENT

    class Meta:
        proxy = True


@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computing_id = models.CharField(max_length=50)

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
