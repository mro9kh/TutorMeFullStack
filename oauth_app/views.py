from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import requests


from .forms import StudentSignUpForm, TutorSignUpForm, addClassForm
from .models import User, Student, Tutor

def addclass(request):
    department = ""
    catalog_number = ""
    message = ""
    if request.method == 'POST':
        formData = request.POST
        form = addClassForm()
        department = (formData["department"]).upper()
        catalog_number = formData["catalog_number"]
        urlQuery = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + department + '&catalog_nbr=' + catalog_number
        response = requests.get(urlQuery)
        sisjson = response.json()
        if len(sisjson)==0:
            message = "is not a valid course in Spring 2023"
        else:
            message = "is a valid course in Spring 2023"
    else:
        form = addClassForm()
    return render(request, 'addclass.html', {'form':form, 'department':department, 'catalog_number': catalog_number, 'message': message})
   
    
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
    

