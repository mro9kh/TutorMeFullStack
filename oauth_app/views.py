from allauth.account.views import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView


# Create your views here.

# allow signup as tutor (model of tutor user)
class TutorSignupView(CreateView):
    model = User
    form_class = TutorSignUpForm  # need a form html
    template_name = ''

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts/home')


# allow signup as student (model of student user)
class StudentSignupView(CreateView):
    model = User
    form_class = StudentSignUpForm  # same as above
    template_name = ''

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts/home')
