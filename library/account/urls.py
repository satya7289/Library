from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import urls

from .views import StudentSignView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    path('signup/student/', StudentSignView.as_view(), name='student_signup'),
]
