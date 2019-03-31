from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.db import connection
from django.template import RequestContext


from account.decorator import student_required
from account.models import Student, Manager, User
from .form import UpdateProfile


# Detail View of individual student
@method_decorator([login_required, student_required], name='dispatch')
class StudentProfile(View):
    template_name = 'student/profile.html'

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        profile = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                   'email': user.email, 'branch': student.Branch, 'roll_no': student.RollNo,
                   'mobile_no': student.MobileNo, 'profile_pic': student.ProfilePicture
                   }
        # print(profile)
        return render(request, self.template_name, {'profile': profile})


@method_decorator([login_required, student_required, ], name='dispatch')
class StudentUpdateProfile(View):
    template_name = 'student/updateProfile.html'
    form_class = UpdateProfile

    def my_custom_sql(self, username):
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email,"
                       "Branch, RollNo, MobileNo, ProfilePicture "
                       "FROM account_user JOIN account_student "
                       "ON account_student.user_id=account_user.id "
                       "WHERE username = %s",
                       [username])
        row = cursor.fetchone()
        return row

    def get(self, request):
        username = request.user.username
        # print(username)
        user = self.my_custom_sql(username)
        print(user[6])
        if user:
            form = self.form_class(initial={'First_name': user[0], 'Last_name': user[1], 'Email': user[2],
                                            'Branch': user[3], 'RollNo': user[4], 'MobileNo': user[5],
                                            'ProfilePicture': user[6]})
            return render(request, self.template_name, {'form': form})
        return render(self.template_name, self.form_class)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        # print(username)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('First_name')
            user.last_name = form.cleaned_data.get('Last_name')
            user.email = form.cleaned_data.get('Email')
            student.Branch = form.cleaned_data.get('Branch')
            student.RollNo = form.cleaned_data.get('RollNo')
            student.MobileNo = form.cleaned_data.get('MobileNo')
            student.ProfilePicture = form.cleaned_data.get('ProfilePicture')
            user.save()
            student.save()
            return redirect('student_profile')











# Update View of individual student
# @method_decorator([login_required, student_required], name='dispatch')
# class UpdateProfilePicture(View):
#     form_class = ProfilePictureChangeForm
#     template_name = 'ProfilePictureChange.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         username = request.User.username
#         user = User.objects.get(username=username)
#         student = Student.objects.get(user=user)
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             student.ProfilePicture = self.cleaned_data.get('UpdateProfilePicture')
#             student.save()
#         return redirect('student_profile')
#

