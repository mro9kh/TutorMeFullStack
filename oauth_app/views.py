from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount
from oauth_app.models import CustomUser

def login_with_google(request):
    # get the socialaccount associated with this request
    social_account = SocialAccount.objects.filter(provider='google', user=request.user).first()

    # check if the user is already logged in and associated with a google account
    if social_account:
        # get the user profile based on the email associated with the google account
        user_profile = CustomUser.objects.filter(email=social_account.extra_data['email']).first()

        # check if the user profile exists and redirect to the appropriate page
        if user_profile:
            if user_profile.user_type == 'student':
                return redirect('student_home')
            elif user_profile.user_type == 'tutor':
                return redirect('tutor_home')
        else:
            return redirect('choose_user_type')

    # if the user is not logged in or not associated with a google account, redirect to google login
    else:
        return redirect('social:begin', 'google-oauth2')

@login_required
def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.user.customuser.user_type = user_type
        request.user.customuser.save()
        if user_type == 'student':
            return redirect('student_home')
        elif user_type == 'tutor':
            return redirect('tutor_home')
    return render(request, 'choose_user_type.html')

@login_required
def student_home(request):
    return render(request, 'student/home.html')

@login_required
def tutor_home(request):
    return render(request, 'tutor/home.html')