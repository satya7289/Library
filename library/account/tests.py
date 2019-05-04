from django.test import TestCase
from .models import Student, Manager, User


class UserTestCase(TestCase):
    def setUp(self):
        self.S1user = User.objects.create(username= 'shyam', password = 'shyam@12345')
        self.S1 = Student.objects.create(user=self.S1user, Branch='CSE', RollNo='B17CS053', MobileNo='8874135787')
        self.S2user = User.objects.create(username='ajay', password='ajay@12345')
        self.S2 = Student.objects.create(user=self.S2user, Branch='ME', RollNo='B17ME008', MobileNo='9588283157')
        self.M1user = User.objects.create(username='sumitsir', password= 'sumit@12345')
        self.M1 = Manager.objects.create(user=self.M1user, CollegeId='PHD01', MobileNo='1234567890', Year='2018')
        self.M2user = User.objects.create(username='joysir', password='joy@12345')
        self.M2 = Manager.objects.create(user=self.M2user, CollegeId='PHD02', MobileNo='1234567891', Year='2019')

    def test_User_datails_1(self):
        self.assertEqual(self.S1user.username, 'shyam')
        self.assertEqual(self.S1user.password, 'shyam@12345')
        self.assertEqual(self.S1.Branch, 'CSE')
        self.assertEqual(self.S1.Branch, "CSE")
        self.assertEqual(self.S1.RollNo, "B17CS053")
        self.assertEqual(self.S1.MobileNo, "8874135787")
        self.assertEqual(self.M1user.username, "sumitsir")
        self.assertEqual(self.M1.CollegeId, "PHD01")
        self.assertEqual(self.M1.MobileNo, "1234567890")
        self.assertEqual(self.M1.Year, "2018")

    def test_User_datails_2(self):
        self.assertEqual(self.S2user.username, 'ajay')
        self.assertEqual(self.S2user.password, 'ajay@12345')
        self.assertEqual(self.S2.Branch, 'ME')
        self.assertEqual(self.S2.RollNo, "B17ME008")
        self.assertEqual(self.S2.MobileNo, "9588283157")
        self.assertEqual(self.M2user.username, "joysir")
        self.assertEqual(self.M2.CollegeId, "PHD02")
        self.assertEqual(self.M2.MobileNo, "1234567891")
        self.assertEqual(self.M2.Year, "2019")