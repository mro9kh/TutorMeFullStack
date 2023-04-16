from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, DecimalValidator
from django.db import transaction
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from .models import Student, Tutor, User, TutoringSession, TutoringRequest


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


class findTutorForm(forms.Form):
    department = forms.CharField(max_length=4)
    catalog_number = forms.CharField(max_length=4)
    classes = Concat('department', V(' '), 'catalog_number', V(''))


# Form class to update profile, like name, year, hour rate
class UpdateTutorProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=Tutor.SCHOOL_YEAR,
                             required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    hourly_rate = forms.DecimalField(max_digits=6, decimal_places=2, required=True,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tutor
        fields = ['name', 'year', 'hourly_rate']


class UpdateStudentProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=Tutor.SCHOOL_YEAR,
                             required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Tutor
        fields = ['name', 'year']


# Form class to be able to create a tutoring session for a specific tutor
class TutoringSessionForm(forms.ModelForm):
    date = forms.DateField()
    time_start = forms.TimeField()
    time_end = forms.TimeField()

    class Meta:
        model = TutoringSession
        exclude = ['tutor']


# Form class that sends tutoring request to tutor
class SendRequestForm(forms.ModelForm):
    message = forms.CharField(max_length=200, required=False,
                              initial='')

    class Meta:
        model = TutoringRequest
        exclude = ['student', 'session', 'status']


# Form that allows tutors to accept requests. It does this by
# changing status of request from False to True
class AcceptRequestForm(forms.ModelForm):
    status = forms.BooleanField(required=None)

    class Meta:
        model = TutoringRequest
        exclude = ['student', 'session', 'message']
