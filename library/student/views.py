from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from account.decorator import student_required
from account.models import Student, Manager, User

#
# # Detail View of individual student
# class StudentProfileDetail(DetailView):
#     model = StudentProfile
#     template_name = 'student/profile.html'
#     pk_url_kwarg = 'pk'
#     context_object_name = 'profile'


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


# Update View of individual student
