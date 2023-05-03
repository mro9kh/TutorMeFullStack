from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.template.defaultfilters import title
from django.utils.text import capfirst


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

    classes = models.TextField(max_length=500, default='')
    random = models.TextField(max_length=500, default='')

    # mail = models.EmailField(unique=True)


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=200)
    SCHOOL_YEAR = [
        ("1", "1st year"),
        ("2", "2nd year"),
        ("3", "3rd year"),
        ("4", "4th year"),
        ("Grad", "Grad Student"),
    ]
    year = models.CharField(max_length=10, choices=SCHOOL_YEAR)
    classes = models.TextField(max_length=500, default='')

    # ---------------
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

    # classes = models.TextField(max_length=1000, default="")
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Capitalize the first letter of each word in the name field
        self.name = title(self.name.lower())
        super(Student, self).save(*args, **kwargs)


#   verify_student = models.BooleanField(default=False)
#   verify_tutor = models.BooleanField(default=False)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField(max_length=200)
    SCHOOL_YEAR = [
        ("1", "1st year"),
        ("2", "2nd year"),
        ("3", "3rd year"),
        ("4", "4th year"),
        ("Grad", "Grad Student"),
        ("Faculty", "Faculty"),
    ]
    year = models.CharField(max_length=10, choices=SCHOOL_YEAR)
    classes = models.TextField(max_length=500, default='')
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    # ---------------
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Capitalize the first letter of each word in the name field
        self.name = title(self.name.lower())
        super(Tutor, self).save(*args, **kwargs)


#   verify_student = models.BooleanField(default=False)
#   verify_tutor = models.BooleanField(default=False)

class TutorClasses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classlist", null=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class StudentClasses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="class_list", null=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Classes(models.Model):
    tutorclass = models.ForeignKey(TutorClasses, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text


# Model for a tutoring session a tutor can create. Each tutor can have multiple tutor sessions,
# but each session is only associated with 1 tutor
class TutoringSession(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutoring_sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError('Start time should be before the end time!')
        return super().clean()


    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=Q(start_time__lte=F('end_time')),
    #             name='start_time_before_end_time')
    #     ]


class TutoringRequest(models.Model):
    session = models.ForeignKey(TutoringSession, on_delete=models.CASCADE, related_name='tutoring_requests')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_requests')
    # message = models.TextField(max_length=200, default='')
    status = models.BooleanField(default=None, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'student'], name='unique_request_per_session')
        ]
