from django.test import TestCase
from .models import User, Student, Tutor

class UserTestCase(TestCase):

    def test_identifies_title(self):
        testTutor = User.objects.create(username= "Henrry", is_student = False, is_tutor=True)
        testStudent = User.objects.create(username= "Jason", is_student = True, is_tutor=False)
        print(testTutor)
        print(testStudent)
        self.assertEqual(testTutor.is_tutor, True)
        self.assertEqual(testStudent.is_student, True)


    def test_student_model(self):
        testStudent = User.objects.create(username="Jason", is_student= True, is_tutor = False)
        test_model = Student.objects.create(user=testStudent, name = "two", year = 3)
        print(test_model = Student.objects.create(user=testStudent, name = "two", year = 3))
        self.assertEqual(test_model.year, 3)
