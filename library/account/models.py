import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


branch = [('CSE', 'Computer Science and Engineering'),
          ('Electrical', 'Electrical Engineering'),
          ('Mechanical', 'Mechanical Engineering'),
          ('Biotechnology', 'BioTechnology Engineering')]

year_choice = []
for r in range(1980, (datetime.datetime.now().year+1)):
    year_choice.append((r, r))


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    Branch = models.CharField(choices=branch, blank=True, null=True, default='CSE', max_length=25)
    RollNo = models.CharField(max_length=10, blank=True, null=True)
    MobileNo = models.CharField(max_length=12)
    ProfilePicture = models.ImageField(upload_to='student/profile/%Y/%m/%d/', blank=True, null=True)

    # class Meta:
    #     ordering = []

    def __str__(self):
        return '%s' % self.user.username


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    CollegeId = models.CharField(max_length=50)
    MobileNo = models.CharField(max_length=12)
    Year = models.IntegerField(choices=year_choice, default=datetime.datetime.now().year)
    ProfilePicture = models.ImageField(upload_to='manager/profile/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return '%s' % self.user.username


