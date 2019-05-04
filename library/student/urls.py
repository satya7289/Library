from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import StudentProfile, StudentUpdateProfile, SearchBook, AddToCartView, CartView, BookView, CheckInView, \
    CheckOutView

urlpatterns = [
    # path('', login_required(TemplateView.as_view(template_name='student/cart.html'), login_url='login'), name=''),

    # update and view profile of individuals
    # path('profile/<int:pk>/', StudentProfileDetail.as_view(), name='student_profile'),
    # path('updateProfile/<int:pk>/', StudentUpdateProfile.as_view(), name='student_UpdateProfile'),

    path('profile/', StudentProfile.as_view(), name='student_profile'),
    path('updateProfile/', StudentUpdateProfile.as_view(), name='student_profile_update'),

    # search
    path('search', SearchBook.as_view(), name='search'),

    # add to cart
    path('add_to_cart/book_no=<book_id>/', AddToCartView.as_view(), name='add_to_cart'),

    # cart view
    path('cart', CartView.as_view(), name='cart'),

    # book view
    path('book', BookView.as_view(), name='student_book'),

    # Check out book
    path('checkIn', CheckOutView.as_view(), name='checkOut_book'),

    # Check In book
    path('checkOut', CheckInView.as_view(), name='checkIn_book'),

]