from django.test import TestCase
from .models import User, Tutor, Student

class UserTestCase(TestCase):
    # def setUp(self):
    #     User.objects.create(is_student= False, is_tutor= True)
    #     User.objects.create(is_student= True, is_tutor= False)
    def test_identifies_title(self):
        student1 = User.objects.create(is_student= False, is_tutor= True)
        student2 = User.objects.create(is_student= True, is_tutor= False)
        self.assertEqual(student1.is_tutor, True)
        self.assertEqual(student2.is_tutor, False)
