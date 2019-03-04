from django.urls import path
from django.views.generic import TemplateView
from .views import RegisterBook,UpdateBook,DeleteBook,BookList,BookDetail

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'manager/home.html'), name='manager_home'),
   # path('book/', TemplateView.as_view(template_name = 'manager/Book.html'), name='book'),
    # Book create/update/delete/detail
    path('registerBook', RegisterBook.as_view(), name='register_book'),
    path('updateBook/<int:update_pk>/', UpdateBook.as_view(), name='update_book'),
    path('deleteBook/<int:delete_pk>/', DeleteBook.as_view(), name='delete_book'),
    path('detailBook/<int:detail_pk>/', BookDetail.as_view(), name='detail_book'),
    path('book/', BookList.as_view(), name='book'),

]