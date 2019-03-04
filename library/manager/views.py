from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Book, Manager_profile
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView , ListView


class RegisterBook(CreateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/createBook.html'
        success_url = reverse_lazy('manager_home')


class UpdateBook(UpdateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/updateBook.html'
        pk_url_kwarg = 'update_pk'
        success_url = reverse_lazy('book')


class DeleteBook(DeleteView):
        model = Book
        pk_url_kwarg = 'delete_pk'
        template_name = 'manager/DeleteBook.html'
        success_url = reverse_lazy('manager_home')


class BookList(ListView):
        model = Book
        paginate_by = 20
        template_name = 'manager/Book.html'
        context_object_name = 'books'


class BookDetail(DetailView):
        model = Book
        template_name = 'manager/BookDetail.html'
        context_object_name = 'book'
        pk_url_kwarg = 'detail_pk'
        #print(Book.objects.count())



