from django.contrib.auth import login, get_user_model, logout
from django.db.models.functions import Concat
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.views.generic import CreateView, ListView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import requests
from django.db.models import CharField, Value as V

from .forms import StudentSignUpForm, TutorSignUpForm, addClassForm, UpdateTutorProfileForm, findTutorForm
from .models import User, Student, Tutor, TutorClasses


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
        sisjsonTotal = response.json()
        if len(sisjsonTotal) == 0:
            message = "is not a valid course in Spring 2023"
        else:
            sisjson = sisjsonTotal[0]
            department = sisjson["subject"]
            catalog_number = sisjson["catalog_nbr"]
            classes = department + catalog_number
            n = request.user
            n.classes = n.classes + "\n" + classes
            n.save()
            # t = TutorClasses(user=n)
            # t.save()
            # request.user.classlist.add(t)
            # tutor = Tutor.objects.filter().first()
            # tutor.classes = tutor.classes + classes + "\n"
            # tutor.save()
            message = "is a valid course in Spring 2023"
            user = get_user_model()
            all_users = User.objects.all()
            print(all_users)
            print(request.user.classes)
            print(request.user)
    else:
        form = addClassForm()
    return render(request, 'addclass.html',
                  {'form': form, 'department': department, 'catalog_number': catalog_number, 'message': message})


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


def tutor_list(request):
    tutors = Tutor.objects.all()
    user = request.user
    print(user.is_student)
    context = {'tutors': tutors}
    # template = loader.get_template('student/home.html')
    return render(request, 'student/home.html', context)


def edit_tutor_profile(request):
    template = 'tutor/profile.html'
    tutor = request.user.tutor
    message = ''
    if request.method == 'POST':
        profile_form = UpdateTutorProfileForm(request.POST, request.FILES, instance=tutor)
        if profile_form.is_valid():
            profile_form.save()
            print(tutor.name)
            message = 'Your profile is updated successfully'
    else:
        profile_form = UpdateTutorProfileForm(instance=tutor)
    return render(request, template, {'profile_form': profile_form, 'message': message})

def find_tutor(request):
    department = ""
    catalog_number = ""
    message = " "
    listOfTutors = []
    template = 'student/find_tutor.html'
    if request.method == 'POST':
        formData = request.POST
        form = findTutorForm()
        department = (formData["department"]).upper()
        catalog_number = formData["catalog_number"]
        classStudent = department + catalog_number #turn into one string
        users = User.objects.all()
        classData = " "
        matches = 0
        for user in users:
            if(user.is_tutor):
                tutorClassString = user.classes
                classData = tutorClassString.split("\n")
            #need to parse classData for classStudent, if match and need to print the tutor
            #check a long string for another string contained within it
            #string.split method? make actual list type
                if classStudent in classData:
                    tutorName = user.tutor.name
                    tutorYear = user.tutor.year
                    tutorClasses = user.classes
                    tutorHourly = user.tutor.hourly_rate
                    toPrint = '\nName: ' + tutorName + " Year: " + tutorYear + " Classes taken: " + tutorClasses + " Hourly Rate: " + tutorHourly
                    listOfTutors.append(user)
                    matches += 1
            
        message = "Number of tutors found for " + classStudent + " are: " + str(matches)

    else:
        form = findTutorForm()
    # get something from data table (json equivalent), parse it, change existing variable if match is made (an array), add that variable to message
    return render(request, 'find_tutor.html',
                  {'form': form, 'department': department, 'catalog_number': catalog_number, 'message': message, 'tutorList': listOfTutors})

"""""
        urlQuery = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + department + '&catalog_nbr=' + catalog_number
        response = requests.get(urlQuery)
        sisjsonTotal = response.json()
        if len(sisjsonTotal) == 0:
            message = "is not a valid course in Spring 2023"
        else:
            sisjson = sisjsonTotal[0]
            department = sisjson["subject"]
            catalog_number = sisjson["catalog_nbr"]
            classes = department + catalog_number
            n = request.user
            n.classes = n.classes + "\n" + classes
            n.save()
            message = "is a valid course in Spring 2023"
            user = get_user_model()
            all_users = User.objects.all()
            print(all_users)
            print(request.user.classes)
            print(request.user)
    else:
        form = addClassForm()
        """
    



def tutor_home(request):
    user = request.user
    tutor = user.tutor
    name = tutor.name
    year = tutor.year
    hourly_rate = tutor.hourly_rate
    context = {'name': name, 'year': year, 'hourly_rate': hourly_rate}
    print(tutor)
    return render(request, 'tutor/home.html', context)

