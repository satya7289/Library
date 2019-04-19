from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, View, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.db import connection
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext


from account.decorator import student_required
from account.models import Student, Manager, User
from manager.models import Book
from .models import Cart
from .form import UpdateProfile


# Detail View of individual student
@method_decorator([login_required, student_required], name='dispatch')
class StudentProfile(View):
    template_name = 'student/profile.html'

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        profile = {'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                   'email': user.email, 'branch': student.Branch, 'roll_no': student.RollNo,
                   'mobile_no': student.MobileNo, 'profile_pic': student.ProfilePicture
                   }
        # print(profile)
        return render(request, self.template_name, {'profile': profile})


@method_decorator([login_required, student_required, ], name='dispatch')
class StudentUpdateProfile(View):
    template_name = 'student/updateProfile.html'
    form_class = UpdateProfile

    def my_custom_sql(self, username):
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email,"
                       "Branch, RollNo, MobileNo, ProfilePicture "
                       "FROM account_user JOIN account_student "
                       "ON account_student.user_id=account_user.id "
                       "WHERE username = %s",
                       [username])
        row = cursor.fetchone()
        return row

    def get(self, request):
        username = request.user.username
        # print(username)
        user = self.my_custom_sql(username)
        print(user[6])
        if user:
            form = self.form_class(initial={'First_name': user[0], 'Last_name': user[1], 'Email': user[2],
                                            'Branch': user[3], 'RollNo': user[4], 'MobileNo': user[5],
                                            'ProfilePicture': user[6]})
            return render(request, self.template_name, {'form': form})
        return render(self.template_name, self.form_class)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        # print(username)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('First_name')
            user.last_name = form.cleaned_data.get('Last_name')
            user.email = form.cleaned_data.get('Email')
            student.Branch = form.cleaned_data.get('Branch')
            student.RollNo = form.cleaned_data.get('RollNo')
            student.MobileNo = form.cleaned_data.get('MobileNo')
            student.ProfilePicture = form.cleaned_data.get('ProfilePicture')
            user.save()
            student.save()
            return redirect('student_profile')

class SearchBook(View):
    template_name = 'student/search.html'
    paginate_by = 2
    model = Book
    context_name = 'books'

    def pagination(self, object):
        paginator = Paginator(object, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            Search = paginator.page(page)
        except PageNotAnInteger:
            Search = paginator.page(1)
        except EmptyPage:
            Search = paginator.page(paginator.num_pages)
        return render(self.request, self.template_name, context={self.context_name: Search})

    def my_custom_sql(self, search):
        cursor = connection.cursor()
        cursor.execute("SELECT book_no, subject, title, author, total, year, CoverPicture, BookPDF"
                       "Branch, RollNo, MobileNo, ProfilePicture "
                       "FROM account_user JOIN account_student "
                       "ON account_student.user_id=account_user.id "
                       "WHERE Branch LIKE %s OR username LIKE %s OR MobileNo LIKE %s",
                       ['%' + search + '%', '%' + search + '%', '%' + search + '%'])
        row = cursor.fetchall()
        return row

    def get(self, request):
        SearchItem = request.GET.get('q')
        if SearchItem == "":
            messages.error(request, 'Search by Book_no,Subject,Title,Author or Year')

        # print(SearchBook)
        if SearchItem:                                            # if Something is in the post method (in search box)
              # if request.user.is_authenticated():                 # if user is authenticated whatever manager or student
              #       username = request.user.username              # Get the username
              #       if request.user.is_student():                 # Check if user is student
              #           pass
              #
              # else:                                                            # if user is not authenticated
                Books = Book.objects.filter(Q(subject__icontains=SearchItem)    # query book by subject, book_no, title
                                                | Q(book_no__icontains=SearchItem)  # author and year
                                                | Q(title__icontains=SearchItem)
                                                | Q(author__icontains=SearchItem)
                                                | Q(year__icontains=SearchItem))
                # print(Books)
                if Books:                                                       # if books found then render result
                    return self.pagination(Books)
                messages.error(request, 'Not found')                             # else raise error not found such query

          # if nothing in the search box then ,
        return render(request, self.template_name)  # search by appropriate query and return


@method_decorator([login_required, student_required, ], name='dispatch')
class AddToCartView(View):

    def my_custom_sql(self, book_id, student):
        cursor = connection.cursor()
        cursor.execute()
        row = cursor.fetchall()
        return row

    def get(self, request, *args, **kwargs):    # check whether current user have previous cart and have not checkout
        bookId = kwargs['book_id']              # then add this book to the cart
        user = request.user
        user_id = request.user.id
        student = Student.objects.get(user=user)
        # self.my_custom_sql(bookId, student)
        return HttpResponse('fdhb')




