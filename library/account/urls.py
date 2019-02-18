from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', TemplateView.as_view(template_name = 'account/login.html'), name='login'),
    path('registration/', TemplateView.as_view(template_name = 'account/registration.html'), name='registration'),


]