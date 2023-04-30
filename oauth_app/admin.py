from django.contrib import admin

# Register your models here.

from .models import Tutor, Student, User, TutoringSession
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(TutoringSession)