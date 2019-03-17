from django.urls import path
from django.views.generic import TemplateView
from .views import StudentProfileDetail, StudentUpdateProfile


urlpatterns = [
    path('', TemplateView.as_view(template_name = 'student/home.html'), name='home'),

    # update and view profile of individuals
    path('profile/<int:pk>/', StudentProfileDetail.as_view(), name='student_profile'),
    path('updateProfile/<int:pk>/', StudentUpdateProfile.as_view(), name='student_UpdateProfile')
]