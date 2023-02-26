from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Student, Tutor, User

class StudentSignUpForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('user', 'name', 'year',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        #student = Student.objects.create(user=user)
        return user
    
class TutorSignUpForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = ('user', 'name', 'year',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_tutor = True
        user.save()
        #tutor = Tutor.objects.create(user=user)
        return user