"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from oauth_app import views
from oauth_app.views import tutor_list, tutor_home

urlpatterns = [
    # path('', include('mysite.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="welcome.html"), name='welcome'),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/choice', TemplateView.as_view(template_name="signup.html"), name='signup'),
    path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/tutor/', views.TutorSignUpView.as_view(), name='tutor_signup'),
    path('accounts/home/student/', tutor_list, name='tutor_list'),
    path('accounts/home/student/', TemplateView.as_view(template_name="student/home.html"), name='student_home'),
    path('accounts/home/tutor/', tutor_home, name='tutor_home'),
    path('accounts/home/tutor/', TemplateView.as_view(template_name="tutor/home.html"), name='tutor_home'),
    path('accounts/home/addclass/', views.addclass, name="addclass"),
    path('accounts/home/tutor/profile', views.edit_tutor_profile, name='tutor_profile'),
    path('accounts/home/tutor/createsession', views.createsession, name="tutoring_session"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
