import datetime
import time
from django.contrib.auth import login, get_user_model, logout
from django.db.models.functions import Concat
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import requests
from django.urls import reverse_lazy
from django.db.models import CharField, Value as V, Q
import calendar
from calendar import HTMLCalendar
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import StudentSignUpForm, TutorSignUpForm, addClassForm, UpdateTutorProfileForm, TutoringSessionForm, \
    UpdateStudentProfileForm, SendRequestForm, findTutorForm, AcceptRequestForm, deleteClassForm, RejectRequestForm, \
    StudentProfilePicForm, TutorProfilePicForm
from .models import User, Student, Tutor, TutorClasses, TutoringSession, TutoringRequest

from django.utils.decorators import method_decorator


class StudentSignUpView(UpdateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=True)
        return redirect('student_home')


@method_decorator(login_required, name='dispatch')
class TutorSignUpView(UpdateView):
    model = User
    form_class = TutorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'tutor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=True)
        return redirect('tutor_home')

def addclass(request):
    department = ""
    catalog_number = ""
    message = ""
    if request.method == 'POST':
        formData = request.POST
        form = addClassForm()
        department = (formData["department"]).upper()
        catalog_number = formData["catalog_number"]
        if department == "" or catalog_number == "":
            # Display an error message and reload the page
            messages.error(request, 'Please do not leave department or catalog number empty')
            return redirect('addclass')
        urlQuery = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + department + '&catalog_nbr=' + catalog_number
        response = requests.get(urlQuery)
        sisjsonTotal = response.json()
        if len(sisjsonTotal) == 0:
            message = "is not a valid course in Spring 2023"
        else:
            sisjson = sisjsonTotal[0]
            department = sisjson["subject"]
            catalog_number = sisjson["catalog_nbr"]
            className = sisjson["descr"]
            newClass = department + catalog_number
            allowed = True
            n = request.user
            classList = n.classes.split()
            for i in classList:
                print(i)
                print(newClass)
                if i == newClass:
                    message = ": " + className + " is already in your profile"
                    allowed = False
            if allowed == True:
                n.classes = n.classes + "\n" + newClass
                n.save()
                message = ": " + className + " was successfully added"
                user = get_user_model()
                all_users = User.objects.all()
                print(all_users)
                print(request.user.classes)
                print(request.user)
    else:
        form = addClassForm()
    return render(request, 'addclass.html',
                  {'form': form, 'department': department, 'catalog_number': catalog_number, 'message': message})


def student_home(request):
    if not request.user.is_authenticated or not request.user.is_student:
        return redirect('welcome')
    tutors = Tutor.objects.prefetch_related('tutoring_sessions').all()
    user = request.user
    student = user.student
    name = student.name
    year = student.year
    tutor_requests = TutoringRequest.objects.filter(student=student, session__date__gte=datetime.date.
                                                    today()).order_by('session__date')
    print(user.is_student)
    context = {'tutors': tutors, 'name': name, 'year': year, 'tutor_requests': tutor_requests}
    # template = loader.get_template('student/home.html')
    return render(request, 'student/home.html', context)


def edit_tutor_profile(request):
    template = 'tutor/profile.html'
    tutor = request.user.tutor
    message = ''
    if request.method == 'POST':
        profile_form = UpdateTutorProfileForm(request.POST, request.FILES, instance=tutor)
        pic_form = TutorProfilePicForm(request.POST, request.FILES, instance=tutor)
        if profile_form.is_valid() and pic_form.is_valid():
            profile_form.save()
            pic_form.save()
            print(tutor.name)
            message = 'Your profile is updated successfully'
    else:
        profile_form = UpdateTutorProfileForm(instance=tutor)
        pic_form = TutorProfilePicForm(instance=tutor)
    return render(request, template, {'profile_form': profile_form, 'message': message, 'pic_form': pic_form})


def edit_student_profile(request):
    template = 'student/profile.html'
    student = request.user.student
    message = ''
    if request.method == 'POST':
        profile_form = UpdateStudentProfileForm(request.POST, request.FILES, instance=student)
        pic_form = StudentProfilePicForm(request.POST, request.FILES, instance=student)
        if profile_form.is_valid():
            profile_form.save()
            pic_form.save()
            print(student.name)
            message = 'Your profile is updated successfully'
    else:
        profile_form = UpdateStudentProfileForm(instance=student)
        pic_form = StudentProfilePicForm(instance=student)
    return render(request, template, {'profile_form': profile_form, 'message': message,
                                      'pic_form': pic_form})


def find_tutor(request):
    department = ""
    catalog_number = ""
    message = " "
    nameMessage = ""
    listOfTutors = []
    validSessions = []
    template = 'student/find_tutor.html'
    if request.method == 'POST':
        formData = request.POST
        form = findTutorForm()
        department = (formData["department"]).upper()
        catalog_number = formData["catalog_number"]
        print(department)
        print(catalog_number)
        if department == "" or catalog_number == "":
            # Display an error message and reload the page
            messages.error(request, 'Please do not leave department or catalog number empty')
            return redirect('find-tutor')
        urlQuery = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + department + '&catalog_nbr=' + catalog_number
        response = requests.get(urlQuery)
        sisjsonTotal = response.json()
        if len(sisjsonTotal) == 0:
            message = department + catalog_number + " is not a valid course in Spring 2023"
        else:
            sisjson = sisjsonTotal[0]
            department = sisjson["subject"]
            catalog_number = sisjson["catalog_nbr"]
            className = sisjson["descr"]
            nameMessage = className
            # *********************************
            classStudent = department + catalog_number  # turn into one string
            users = User.objects.all()
            sessions = TutoringSession.objects.all()
            classData = " "
            matches = 0
            for user in users:
                if (user.is_tutor):
                    tutorClassString = user.classes
                    classData = tutorClassString.split("\n")
                    if classStudent in classData:
                        listOfTutors.append(user)
                        matches += 1
                        for session in sessions:
                            if session.tutor_id == user.tutor.user_id:
                                validSessions.append(session)
            message = "Number of tutors found for " + classStudent + ": " + nameMessage + " are: " + str(matches)
                # *********************
    else:
        form = findTutorForm()
    return render(request, 'find_tutor.html',
                  {'form': form, 'department': department, 'catalog_number': catalog_number, 'message': message,
                   'tutorList': listOfTutors, 'sessions': validSessions, 'nameMessage': nameMessage})


def tutor_home(request):
    if not request.user.is_authenticated or not request.user.is_tutor:
        return redirect('welcome')
    user = request.user
    tutor = user.tutor
    name = tutor.name
    year = tutor.year
    hourly_rate = tutor.hourly_rate
    tutoring_sessions = TutoringSession.objects.filter(tutor=tutor).order_by('date')
    context = {'name': name, 'year': year, 'hourly_rate': hourly_rate, 'sessions': tutoring_sessions}
    print(tutor)
    print(tutoring_sessions)
    return render(request, 'tutor/home.html', context)


# Process and create a tutoring session
def createsession(request):
    template = 'tutor/createsession.html'
    tutor = request.user.tutor
    message = ''
    if request.method == 'POST':
        tutoring_form = TutoringSessionForm(request.POST, request.FILES, request=request)
        if tutoring_form.is_valid():
            tutoring_session = tutoring_form.save(commit=False)
            tutoring_session.tutor = tutor
            tutoring_session.save()
            print(tutor)
            print(tutoring_form.errors)
            message = 'Your session was created successfully'
    else:
        tutoring_form = TutoringSessionForm(request=request)
    return render(request, template, {'tutoring_form': tutoring_form, 'message': message})


def send_request(request, tutor):
    uid = User.objects.get(username=tutor)
    current_session_id = None
    message = ''
    tutor = uid.tutor
    name = tutor.name
    tutor_username = tutor.user.username
    tutoring_sessions = TutoringSession.objects.filter(tutor=tutor, date__gte=datetime.date.today()).order_by('date')
    tutoring_requests = TutoringRequest.objects.filter(student=request.user.student)

    # this checks to see if a session already has a request
    for session in tutoring_sessions:
        has_request = tutoring_requests.filter(session=session, student=request.user.student).exists()
        # session.has_request = has_request
        request_status = None
        # this checks the status of the request
        if has_request:
            request_status = tutoring_requests.get(session=session, student=request.user.student).status
            print(request_status)
        session.has_request = has_request
        session.request_status = request_status

        #     print(request_status)
        # session.has_request = has_request
        # session.request = None if not has_request else tutoring_requests.get(session=session,
        #                                                                      student=request.user.student)
        # session.request.status = request_status if request_status is not None else None
        # print(session.has_request)
    # print(tutoring_sessions)
    # print(session.has_request)
    if request.method == "POST":
        form = SendRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # print(request.POST['session_id'])
            # Check if the user has already requested this session
            session_id = request.POST['session_id']
            existing_request = TutoringRequest.objects.filter(session_id=session_id,
                                                              student=request.user.student).exists()
            if existing_request:
                # Display an error message and reload the page
                messages.error(request, 'You have already requested this session.')
                return redirect('request', tutor=tutor_username)

            tutor_request = form.save(commit=False)
            tutor_request.status = None
            tutor_request.student = request.user.student
            tutor_request.session = TutoringSession.objects.get(pk=request.POST['session_id'])
            current_session_id = tutor_request.session.id
            # print(current_session_id)
            tutor_request.save()
            message = "Request sent to " + tutor_username + '!'
            for session in tutoring_sessions:
                has_request = tutoring_requests.filter(session=session, student=request.user.student).exists()
                request_status = None
                if has_request:
                    request_status = tutoring_requests.get(session=session, student=request.user.student).status
                    print(request_status)
                session.has_request = has_request
                session.request_status = request_status
            # return redirect('request', tutor=tutor_username)
    else:
        form = SendRequestForm(initial={'student': request.user.student, 'session': tutoring_sessions.first().id})
    return render(request, 'student/request.html', {'name': name,
                                                    'user': uid,
                                                    'tutor': tutor,
                                                    'sessions': tutoring_sessions,
                                                    'username': tutor_username,
                                                    'form': form,
                                                    'message': message,
                                                    'current_session_id': current_session_id,
                                                    'tutoring_requests': tutoring_requests})


def pending_requests(request):
    template = 'tutor/pending_requests.html'
    message = ''
    tutor = request.user.tutor
    tutoring_requests = TutoringRequest.objects.filter(session__tutor=tutor, status=None,
                                                       session__date__gte=datetime.date.today())
    if request.method == "POST":
        if 'accept' in request.POST:
            form = AcceptRequestForm(request.POST, request.FILES)
            if form.is_valid():
                # print(form.cleaned_data.keys())
                print(request.POST['tutoring_request_id'])
                tutor_request = TutoringRequest.objects.get(pk=request.POST['tutoring_request_id'])
                tutor_request.status = True
                tutor_request.save()
                message = "Request Accepted! " + tutor_request.student.name + " is now in your session."
                print(tutor_request.status)
                print(tutor_request.session.date)
            # return redirect('pending_requests')
        elif 'reject' in request.POST:
            form = RejectRequestForm(request.POST, request.FILES)
            if form.is_valid():
                print(request.POST['tutoring_request_id'])
                tutor_request = TutoringRequest.objects.get(pk=request.POST['tutoring_request_id'])
                tutor_request.status = False
                tutor_request.save()
                message = "Request Rejected!"
                print(tutor_request.status)
                print(tutor_request.session.date)
    else:
        form = SendRequestForm()
    return render(request, template, {'tutoring_requests': tutoring_requests, 'form': form, 'message': message})


def student_pending_requests(request):
    template = 'student/pending_requests.html'
    tutors = Tutor.objects.prefetch_related('tutoring_sessions').all()
    user = request.user
    student = user.student
    name = student.name
    year = student.year
    tutor_requests = TutoringRequest.objects.filter(student=student, session__date__gte=datetime.date.
                                                    today()).order_by('session__date')
    print(user.is_student)
    context = {'tutors': tutors, 'name': name, 'year': year, 'tutor_requests': tutor_requests}
    return render(request, template, context)


def schedule(request):
    template = 'tutor/schedule.html'
    tutor = request.user.tutor
    tutoring_schedule = TutoringRequest.objects.filter(session__tutor=tutor, status=True,
                                                       session__date__gte=datetime.date.
                                                       today()).order_by('session__date')
    return render(request, template, {'tutoring_schedule': tutoring_schedule})


def student_schedule(request):
    tutors = Tutor.objects.prefetch_related('tutoring_sessions').all()
    user = request.user
    student = user.student
    name = student.name
    year = student.year
    tutor_requests = TutoringRequest.objects.filter(student=student, session__date__gte=datetime.date.
                                                    today()).order_by('session__date')
    print(user.is_student)
    context = {'tutors': tutors, 'name': name, 'year': year, 'tutor_requests': tutor_requests}
    template = 'student/schedule.html'
    return render(request, template, context)


def delete_class(request):
    user = request.user
    department = ""
    catalog_number = ""
    message = ""
    rawClasses = user.classes
    classes = rawClasses.split()
    if request.method == 'POST':
        formData = request.POST
        form = deleteClassForm()
        department = (formData["department"]).upper()
        catalog_number = formData["catalog_number"]
        if department == "" or catalog_number == "":
            # Display an error message and reload the page
            messages.error(request, 'Please do not leave department or catalog number empty')
            return redirect('delete-class')
        urlQuery = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=' + department + '&catalog_nbr=' + catalog_number
        response = requests.get(urlQuery)
        sisjsonTotal = response.json()
        if len(sisjsonTotal) == 0:
            message = "is not a valid course in Spring 2023"
        else:
            sisjson = sisjsonTotal[0]
            department = sisjson["subject"]
            catalog_number = sisjson["catalog_nbr"]
            className = sisjson["descr"]
            # *********************************************
            classToDelete = department + catalog_number
            found = False
            for i in classes:
                if (i == classToDelete):
                    classes.remove(classToDelete)
                    found = True
                    message = ": " + className + " has been deleted from your profile"
            if found == False:
                message = ": " + className + " was not found in your profile"
            n = request.user
            n.classes = ""
            if len(classes) == 0:
                n.classes = ""
                n.save()
            else:
                for j in classes:
                    n.classes = n.classes + "\n" + j
                    n.save()
                    # ***********************
    else:
        form = deleteClassForm()
    return render(request, 'delete_class.html',
                  {'form': form, 'department': department, 'catalog_number': catalog_number, 'message': message,
                   'classes': classes})
