from django.urls import path
from django.views.generic import TemplateView
from .views import RegisterBook, UpdateBook, DeleteBook, BookList, BookDetail, ManagerProfile, Search, \
    SearchStudentView, ManagerUpdateProfile, StudentListAndDetailView


urlpatterns = [
    path('', TemplateView.as_view(template_name='manager/home.html'), name='manager_home'),

    # Book create/update/delete/detail
    path('registerBook', RegisterBook.as_view(), name='register_book'),
    path('updateBook/<int:update_pk>/', UpdateBook.as_view(), name='update_book'),
    path('deleteBook/<int:delete_pk>/', DeleteBook.as_view(), name='delete_book'),
    path('detailBook/<int:detail_pk>/', BookDetail.as_view(), name='detail_book'),
    path('book/', BookList.as_view(), name='book'),

    # Manager update and profile
    path('profile/', ManagerProfile.as_view(), name='manager_profile'),
    path('updateProfile/', ManagerUpdateProfile.as_view(), name='manager_update_profile'),

    # search book
    path('search?=book', Search.as_view(), name='search_book'),

    # student list
    path('studentList', StudentListAndDetailView.as_view(), name='studentList'),
    path('search?=student&', SearchStudentView.as_view(), name='search_student'),
    # path('student/detail/(?P<username>\w{0,50})/$', StudentDetailView.as_view(), name='student_detail'),


]
