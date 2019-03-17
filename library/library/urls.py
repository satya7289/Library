from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="base.html"), name='base'),
    path('account/', include('account.urls')),
    path('student/', include('student.urls')),
    path('manager/', include('manager.urls')),

    # api for book
    path('api/manager/', include('manager.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
