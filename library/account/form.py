import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import User
from .models import Student, Manager, branch, year_choice


class StudentSignUpForm(UserCreationForm):
    Branch = forms.ChoiceField(choices=branch, required=False)
    RollNo = forms.CharField(max_length=10,)
    MobileNo = forms.CharField(max_length=12)
    profilePicture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.Branch = self.cleaned_data.get('Branch')
        student.RollNo = self.cleaned_data.get('RollNo')
        student.MobileNo = self.cleaned_data.get('MobileNo')
        student.ProfilePicture = self.cleaned_data('ProfilePicture')
        student.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)






# class ManagerSignupForm(UserCreationForm):
#     CollegeId = forms.CharField(max_length=50)
#     MobileNo = forms.CharField(max_length=12)
#     Year = forms.ChoiceField(choices=year_choice)
#     ProfilePicture = forms.ImageField(required=False)
#
#     class Meta(UserCreationForm.Meta):
#         model = User
#
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_manager = True
#         user.save()
#         manger = Manager.objects.create(user=user)
#         manger.CollegeId = self.cleaned_data.get('CollegeId')
#         manger.MobileNo = self.cleaned_data.get('MobileNo')
#         manger.Year.add = self.cleaned_data.get('Year')
#         manger.ProfilePicture = self.cleaned_data.get('ProfilePicture')
#         manger.save()
#         return user

