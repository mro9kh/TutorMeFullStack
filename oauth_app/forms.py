import datetime
from django import forms
from django.db import transaction
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.contrib.auth import get_user_model
from django.forms import TimeInput
from django.utils.translation import gettext_lazy as _

from .models import Student, Tutor, User, TutoringSession, TutoringRequest

User = get_user_model()


class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = self.instance.username
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        if user.id:  # If the user already exists in the database
            user.is_student = True
            user.set_unusable_password()
            user.save()
            student, _ = Student.objects.get_or_create(user=user)
            student.save()
        else:  # If the user doesn't exist yet
            user = super().save(commit=True)
            user.is_student = True
            user.set_unusable_password()
            user.save()
            student = Student.objects.create(user=user)
            student.save()  # Save the related object
        return user


class TutorSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['username'] = self.instance.username
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = self.instance
        if user.id:  # If the user already exists in the database
            user.is_tutor = True
            user.set_unusable_password()
            user.save()
            tutor, _ = Tutor.objects.get_or_create(user=user)
            tutor.save()
        else:  # If the user doesn't exist yet
            user = super().save(commit=True)
            user.is_tutor = True
            user.set_unusable_password()
            user.save()
            tutor = Tutor.objects.create(user=user)
            tutor.save()  # Save the related object
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
    year = forms.ChoiceField(choices=Student.SCHOOL_YEAR,
                             required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Tutor
        fields = ['name', 'year']


def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


# Form class to be able to create a tutoring session for a specific tutor
class TutoringSessionForm(forms.ModelForm):
    date = forms.DateField(validators=[present_or_future_date], input_formats=['%d/%m/%Y'])
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(
        attrs={'class': 'form-control timepicker', 'autocomplete': 'off'}),
                                 input_formats=['%I:%M %p'])
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(
        attrs={'class': 'form-control timepicker', 'autocomplete': 'off'}),
                               input_formats=['%I:%M %p'])

    class Meta:
        model = TutoringSession
        fields = ['date', 'start_time', 'end_time']


# Form class that sends tutoring request to tutor
class SendRequestForm(forms.ModelForm):
    # message = forms.CharField(max_length=200, required=False,
    #                           initial='')

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
