from django.test import TestCase
from .models import User, Student, Tutor

class UserTestCase(TestCase):
   def test_user_student(self):
       randoUser = User.objects.create(username="testStudent", is_tutor = False, is_student= True)
       self.assertEqual(randoUser.is_student, True)
  
   def test_user_tutor(self):
       randoUser = User.objects.create(username="testTutor", is_tutor = True, is_student= False)
       self.assertEqual(randoUser.is_tutor, True)

   def test_user_both_isStudent(self):
       randoUser = User.objects.create(username="testStudent", is_tutor = True, is_student= True)
       self.assertEqual(randoUser.is_student, True)

   def test_user_both_isTutor(self):
       randoUser = User.objects.create(username="testTutor", is_tutor = True, is_student= True)
       self.assertEqual(randoUser.is_tutor, True)

   def test_student_model(self):
       randoUser = User.objects.create(username="testStudent", is_tutor = False, is_student= True)
       test_model = Student.objects.create(user=randoUser, name = "two", year = 3)
       self.assertEqual(test_model.year, 3)

   def test_tutor_model(self):
       randoUser = User.objects.create(username="testTutor", is_tutor = True, is_student= False)
       test_model = Tutor.objects.create(user=randoUser, name = "two", year = 3)
       self.assertEqual(test_model.year, 3)

    