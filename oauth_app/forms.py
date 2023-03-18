from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from .models import Student, Tutor, User


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TutorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutor = True
        user.save()
        tutor = Tutor.objects.create(user=user)
        return user


class addClassForm(forms.Form):
    department = forms.CharField(max_length=4)
    catalog_number = forms.CharField(max_length=4)
    classes = Concat('department', V(' '), 'catalog_number', V(''))
