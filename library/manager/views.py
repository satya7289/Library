from django.urls import reverse_lazy
from .models import Book, ManagerProfile
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView, View
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages


# Manager Profile Detail View from backend to frontend
class ManagerProfileDetail(DetailView):
        model = ManagerProfile
        context_object_name = 'profile'
        pk_url_kwarg = 'manager_pk'
        template_name = 'manager/profile.html'


# Updating Manager Profile Detail View from frontend to backend
class ManagerProfileUpdate(UpdateView):
        model = ManagerProfile
        fields = ['name', 'college_id', 'email', 'mobile_no', 'year']
        template_name = 'manager/updateProfile.html'
        pk_url_kwarg = 'manager_pk'

        def get_success_url(self):
                pk = self.kwargs['manager_pk']
                return reverse_lazy('manager_profile', kwargs={'manager_pk': pk})


# updating Profile Picture
# not working now
class UpdateProfilePicture(UpdateView):
        model = ManagerProfile
        fields = [' profile_picture']
        template_name = 'manager/updateProfile.html'
        pk_url_kwarg = 'manager_pk'
        success_url = reverse_lazy('manager_profile')


# Registering/creating Book View via frontend to backend
class RegisterBook(CreateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/createBook.html'
        success_url = reverse_lazy('manager_home')


# Updating Book View via frontend to backend
class UpdateBook(UpdateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/updateBook.html'
        pk_url_kwarg = 'update_pk'
        success_url = reverse_lazy('book')


# Deletion of Book View via frontend to backend
class DeleteBook(DeleteView):
        model = Book
        pk_url_kwarg = 'delete_pk'
        template_name = 'manager/DeleteBook.html'
        success_url = reverse_lazy('manager_home')


# Listing of Book View from backend to frontend
class BookList(ListView):
        model = Book
        paginate_by = 20
        template_name = 'manager/Book.html'
        context_object_name = 'books'


# Detail of Book View from backend to frontend
class BookDetail(DetailView):
        model = Book
        template_name = 'manager/BookDetail.html'
        context_object_name = 'book'
        pk_url_kwarg = 'detail_pk'
        #print(Book.objects.count())


# Searching Book View
class Search(View):

        def get(self, request):
                return render(request, 'manager/Book.html')

        def post(self, request):
                searchItem = request.POST['search']
                if searchItem:
                        #print(searchItem)
                        Books = Book.objects.filter(Q(subject__icontains=searchItem)
                                                    |Q(book_no__icontains=searchItem)
                                                    |Q(title__icontains=searchItem)
                                                    |Q(author__icontains=searchItem)
                                                    |Q(year__icontains=searchItem))
                       # print(Books)
                        if Books:
                                return render(request, 'manager/Book.html', context={'books': Books})
                        messages.error(request, 'Not found')
                messages.error(request, 'Search by Book_no,Subject,Title,Author or Year')
                return render(request, 'manager/Book.html')




