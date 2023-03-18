from django.test import TestCase
from oauth_app.models import User

class UserTestCase(TestCase):

    def test_identifies_title(self):
        ya = User.objects.create(username= "Henrry", is_student = False, is_tutor=True)
        yeet = User.objects.create(username= "Jason", is_student = True, is_tutor=False)
        print(ya)
        print(yeet)
        self.assertEqual(ya.is_tutor, True)
        self.assertEqual(yeet.is_student, True)


