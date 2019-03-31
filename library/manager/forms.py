from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db import transaction


from account.models import Student,User
from account.models import year_choice


class UpdateManagerProfile(forms.Form):
    First_name = forms.CharField(required=False)
    Last_name = forms.CharField(required=False)
    Email = forms.EmailField(required=False)
    CollegeId = forms.CharField(max_length=50)
    MobileNo = forms.CharField(max_length=12)
    Year = forms.ChoiceField(choices=year_choice)
    ProfilePicture = forms.ImageField(required=False)


