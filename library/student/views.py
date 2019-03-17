from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView
from .models import StudentProfile


# Detail View of individual student
class StudentProfileDetail(DetailView):
    model = StudentProfile
    template_name = 'student/profile.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'profile'


# Update View of individual student
class StudentUpdateProfile(UpdateView):
    model = StudentProfile
    template_name = 'student/updateProfile.html'
    pk_url_kwarg = 'pk'
    fields = ['FirstName', 'MiddleName', 'LastName', 'Branch', 'RollNo', 'Email', 'Mobile']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('student_UpdateProfile', kwargs={'pk': pk})
