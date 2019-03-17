from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views


urlpatterns = [
    path('book/', api_views.BookApiList.as_view()),
    path('book/<int:pk>/', api_views.BookApiDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)