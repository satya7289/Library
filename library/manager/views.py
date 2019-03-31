from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView, View
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import Http404


from .models import Book
from account.decorator import manager_required
from account.models import Manager, User, Student
from .forms import UpdateManagerProfile


# Manager Profile Detail View from backend to frontend
@method_decorator([login_required, manager_required], name='dispatch')
class ManagerProfile(View):
    template_name = 'manager/profile.html'

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        manager = Manager.objects.get(user=user)
        profile = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                   'email': user.email, 'college_id': manager.CollegeId, 'mobile_no': manager.MobileNo,
                   'year': manager.Year, 'profile_pic': manager.ProfilePicture
                   }
        # print(profile)
        return render(request, self.template_name, {'profile': profile})


# Update Manager Profile View
@method_decorator([login_required, manager_required], name='dispatch')
class ManagerUpdateProfile(View):
    template_name = 'manager/updateProfile.html'
    form_class = UpdateManagerProfile

    def my_custom_sql(self, username):
        cursor = connection.cursor()
        cursor.execute("SELECT first_name,last_name,email,"
                       "CollegeId, MobileNo, Year, ProfilePicture FROM account_user JOIN account_manager ON"
                       " account_manager.user_id = account_user.id WHERE username=%s", [username]
                       )
        row = cursor.fetchone()
        return row

    def get(self, request):
        username = request.user.username
        # print(username)
        user = self.my_custom_sql(username)
        if user:
            form = self.form_class(initial={'First_name': user[0], 'Last_name': user[1], 'Email': user[2],
                                            'CollegeId': user[3], 'MobileNo': user[4], 'Year': user[5],
                                            'ProfilePicture': user[6]})
            return render(request, self.template_name, {'form': form})
        return render(self.template_name, self.form_class)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        manager = Manager.objects.get(user=user)
        # print(username)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('First_name')
            user.last_name = form.cleaned_data.get('Last_name')
            user.email = form.cleaned_data.get('Email')
            manager.CollegeId = form.cleaned_data.get('CollegeId')
            manager.Year = form.cleaned_data.get('Year')
            manager.MobileNo = form.cleaned_data.get('MobileNo')
            manager.ProfilePicture = form.cleaned_data.get('ProfilePicture')
            user.save()
            manager.save()
            return redirect('manager_profile')


# Registering/creating Book View via frontend to backend
@method_decorator([login_required, manager_required], name='dispatch')
class RegisterBook(CreateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/createBook.html'
        success_url = reverse_lazy('book')


# Updating Book View via frontend to backend
@method_decorator([login_required, manager_required], name='dispatch')
class UpdateBook(UpdateView):
        model = Book
        fields = ['book_no', 'subject', 'title', 'author', 'total', 'year']
        template_name = 'manager/updateBook.html'
        pk_url_kwarg = 'update_pk'
        success_url = reverse_lazy('book')


# Deletion of Book View via frontend to backend
@method_decorator([login_required, manager_required], name='dispatch')
class DeleteBook(DeleteView):
        model = Book
        pk_url_kwarg = 'delete_pk'
        template_name = 'manager/DeleteBook.html'
        success_url = reverse_lazy('book')


# Listing of Book View from backend to frontend
@method_decorator([login_required, manager_required], name='dispatch')
class BookList(ListView):
        model = Book
        paginate_by = 20
        template_name = 'manager/Book.html'
        context_object_name = 'books'


# Detail of Book View from backend to frontend
@method_decorator([login_required, manager_required], name='dispatch')
class BookDetail(DetailView):
        model = Book
        template_name = 'manager/BookDetail.html'
        context_object_name = 'book'
        pk_url_kwarg = 'detail_pk'
        # print(Book.objects.count())


# Searching Book View
@method_decorator([login_required, manager_required], name='dispatch')
class Search(View):

        def get(self, request):
                return render(request, 'manager/Book.html')

        def post(self, request):
                searchItem = request.POST['search']
                if searchItem:
                        # print(searchItem)
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


# List of all student Register in the web portal
@method_decorator([login_required, manager_required], name='dispatch')
class StudentListView(ListView):

        def my_custom_sql(self):
            cursor = connection.cursor()
            cursor.execute("SELECT username, first_name, last_name, email,"
                           "Branch, RollNo, MobileNo, ProfilePicture "
                           "FROM account_user JOIN account_student "
                           "ON account_student.user_id=account_user.id")
            row = cursor.fetchall()
            return row

        model = User
        queryset = my_custom_sql(model)
        paginate_by = 20
        template_name = 'manager/student.html'
        context_object_name = 'students'
        #print(queryset)


# detail of individual students
@method_decorator([login_required, manager_required], name='dispatch')
class StudentDetailView(View):
    template_name = 'manager/studentDetail.html'

    def my_custom_sql(self,username):
        cursor = connection.cursor()
        cursor.execute("SELECT username, first_name, last_name, email,"
                       "Branch, RollNo, MobileNo, ProfilePicture "
                       "FROM account_user JOIN account_student "
                       "ON account_student.user_id=account_user.id"
                       "WHERE username=%s", [username])
        row = cursor.fetchone()
        return row

    def get(self, request, *args, **kwargs):
        # username = request.GET.get('username', None)
        # student = self.my_custom_sql(username)
        # if student:
        #     return render(request, self.template_name, {'profile': student})
        # raise Http404
        pass


# search student on manager side
@method_decorator([login_required, manager_required], name='dispatch')
class SearchStudentView(View):

    def get(self, request):
        return render(request, 'manager/student.html')

    def my_custom_sql(self, search):
        cursor = connection.cursor()
        cursor.execute("SELECT username, first_name, last_name, email,"
                       "Branch, RollNo, MobileNo, ProfilePicture "
                       "FROM account_user JOIN account_student "
                       "ON account_student.user_id=account_user.id "
                       "WHERE Branch LIKE %s OR username LIKE %s OR MobileNo LIKE %s",
                       ['%' + search + '%', '%' + search + '%', '%' + search + '%'])
        row = cursor.fetchall()
        return row

    def post(self, request):
        searchItem = request.POST['search']
        if searchItem:
            students = self.my_custom_sql(searchItem)
            # print(students)
            if students:
                return render(request, 'manager/student.html', context={'students': students})
            messages.error(request, 'Not found')
        messages.error(request, 'Search by username, email, Branch')
        return render(request, 'manager/student.html')
