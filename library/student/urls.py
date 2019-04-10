from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import StudentProfile, StudentUpdateProfile, SearchBook

urlpatterns = [
    #path('', login_required(TemplateView.as_view(template_name='student/search.html'), login_url='login'), name=''),

    # update and view profile of individuals
    # path('profile/<int:pk>/', StudentProfileDetail.as_view(), name='student_profile'),
    # path('updateProfile/<int:pk>/', StudentUpdateProfile.as_view(), name='student_UpdateProfile'),

    path('profile/', StudentProfile.as_view(), name='student_profile'),
    path('updateProfile/', StudentUpdateProfile.as_view(), name='student_profile_update'),

    # search
    path('search', SearchBook.as_view(), name='search'),

]