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

    # def my_custom_sql(self, search):
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT book_no, subject, title, author, total, year, CoverPicture, BookPDF"
    #                    "Branch, RollNo, MobileNo, ProfilePicture "
    #                    "FROM account_user JOIN account_student "
    #                    "ON account_student.user_id=account_user.id "
    #                    "WHERE Branch LIKE %s OR username LIKE %s OR MobileNo LIKE %s",
    #                    ['%' + search + '%', '%' + search + '%', '%' + search + '%'])
    #     row = cursor.fetchall()
    #     return row

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


def search_user_cart_sql(userid, checkin, checkout):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM student_cart WHERE CheckOut=%s and User_id=%s and CheckIn=%s",
                   [checkout, userid, checkin])
    row = cursor.fetchall()
    return row

@method_decorator([login_required, student_required, ], name='dispatch')
class AddToCartView(View):

    def add_book_to_cart_sql(self, cart_id, book_id):
        cursor = connection.cursor()
        success = 0
        try:
            cursor.execute("INSERT INTO student_cart_Book(cart_id,book_id) VALUES (%s,%s)", [cart_id, book_id])
            success = 1
        except:
            success = 0
        return success

    def create_user_cart_sql(self, user_id, checkin, checkout):
        cursor = connection.cursor()
        success = 0
        try:
            cursor.execute("INSERT INTO student_cart(CheckIn,CheckOut,User_id) VALUES (%s,%s,%s)",
                           [checkin, checkout, user_id])
            success = 1
        except:
            success = 0
        return success



    def last_row_insert_sql(self):
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ROWID()")
        row = cursor.fetchone()
        return row

    def get(self, request, *args, **kwargs):    # check whether current user have previous cart and have not checkout
        book_id = kwargs['book_id']              # then add this book to the cart
        student = Student.objects.get(user=request.user)
        cart = search_user_cart_sql(student.user_id, 0, 0)
        if cart == []:
            success = self.create_user_cart_sql(student.user_id, 0, 0)
            cart_id = self.last_row_insert_sql()
            success_book_report = self.add_book_to_cart_sql(cart_id[0], book_id)
            print("satya", success, success_book_report)
        else:
            cart_id = cart[0][0]
            success = self.add_book_to_cart_sql(cart_id, book_id)
            print(success)

        # print(book_id, student, student.user_id, cart)
        return redirect('cart')


@method_decorator([login_required, student_required, ], name='dispatch')
class CartView(View):
    template_name = 'student/cart.html'
    context_name = 'books'

    def search_book_according_to_cart(self, card_id):
        cursor = connection.cursor()
        cursor.execute("SELECT book_no,subject,title,author,total,year,CoverPicture,BookPDF FROM manager_book "
                       "JOIN student_cart_Book ON manager_book.id=student_cart_Book.book_id WHERE cart_id=%s", [card_id])
        row = cursor.fetchall()
        return row

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        cart = search_user_cart_sql(student.user_id, 0, 0)
        cart_id = cart[0][0]
        books = self.search_book_according_to_cart(cart_id)
        # print(cart_id)
        # print(books)
        return render(self.request, self.template_name, context={self.context_name: books})


@method_decorator([login_required, student_required, ], name='dispatch')
class CheckOutView(View):

    def checkout_sql(self, cart_id):
        cursor = connection.cursor()
        cursor.execute("UPDATE student_cart SET CheckOut=1 WHERE id=%s", [cart_id])
        return

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        cart = search_user_cart_sql(student.user_id, 0, 0)
        cart_id = cart[0][0]
        self.checkout_sql(cart_id)
        return redirect('book')


@method_decorator([login_required, student_required, ], name='dispatch')
class CheckInView(View):

    def checkIn_sql(self, cart_id):
        cursor = connection.cursor()
        cursor.execute("UPDATE student_cart SET CheckIn=1 WHERE id=%s", [cart_id])
        return

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        cart = search_user_cart_sql(student.user_id, 0, 1)
        cart_id = cart[0][0]
        self.checkIn_sql(cart_id)
        return redirect('student_profile')


@method_decorator([login_required, student_required, ], name='dispatch')
class BookView(View):
    # template_name = 'student/book.html'
    # context_name = 'books'
    #
    # def search_book_according_to_cart(self, card_id):
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT book_no,subject,title,author,total,year,CoverPicture,BookPDF FROM manager_book "
    #                    "JOIN student_cart_Book ON manager_book.id=student_cart_Book.book_id WHERE cart_id=%s",
    #                    [card_id])
    #     row = cursor.fetchall()
    #     return row
    #
    # def get(self, request, *args, **kwargs):
    #     student = Student.objects.get(user=request.user)
    #     cart = search_user_cart_sql(student.user_id, 0, 1)
    #     cart_id = cart[0][0]
    #     books = self.search_book_according_to_cart(cart_id)
    #     # print(cart_id)
    #     # print(books)
    #     return render(self.request, self.template_name, context={self.context_name: books})
    pass


