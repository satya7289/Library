from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="base.html"), name='base'),
    path('account/', include('account.urls')),
    path('student/', include('student.urls')),
    path('manager/', include('manager.urls')),
]

