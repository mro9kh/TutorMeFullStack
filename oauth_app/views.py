from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import requests


from .forms import StudentSignUpForm, TutorSignUpForm
from .models import User, Student, Tutor

def addclass(request):
    response = requests.get('https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=CS&catalog_nbr=1110')
    sisjson = response.json()
    if len(sisjson)==0:
        return render(request, 'addclass.html', {
        'department': "Not Found",
        'catalog_number': "Not Found"
    })
    else:
        sisdata = sisjson[0]
        return render(request, 'addclass.html', {
            'department': sisdata["subject"],
            'catalog_number': sisdata["catalog_nbr"]
        })
class StudentSignUpView(CreateView):
    model = Student
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('student_home')
    
class TutorSignUpView(CreateView):
    model = User
    form_class = TutorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('tutor_home')
    

