from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, CreateView
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .form import StudentSignUpForm, LoginForm
from .models import Student,Manager, User


class StudentSignView(CreateView):
    template_name = 'account/registration.html'
    model = User
    form_class = StudentSignUpForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student_profile')


class LoginView(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
        # print(username, password, 'vnv')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_manager:
                login(request, user)
                return redirect('manager_profile')
            elif user.is_student:
                login(request, user)
                return redirect('student_profile')
        return render(request, self.template_name, {'form': form},
                      messages.error(request, 'Enter correct username and password'))



# class LoginView(View):
#     template_name = 'account/login.html'
#     # form_class = LoginForm
#
#     def get(self, request):
#         # form = self.form_class(None)
#         return render(request, self.template_name)
#
#     def post(self, request):
#         # form = self.form_class(request.POST)
#         # print(form)
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # print(username, password, 'vnv')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_manager:
#                 login(request, user)
#                 # print('manager')
#                 return redirect('manager_home')
#             elif user.is_student:
#                 login(request, user)
#                 # print('student')
#                 return redirect('home')
#             # elif user.is_superuser:
#             #     login(request, user)
#             #     print('superuser')
#             #     return HttpResponse("superuserlogin")
#         return render(request, self.template_name, messages.error(request, 'Enter correct username and password') )
#
#
# print(User.is_authenticated, User.get_username, 'fbjh')

        # form = self.form_class(request.POST)
        #
        # if form.is_valid():
        #     user = form.save(commit=False)
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #     user.set_password(password)
        #     user.save()
        #     user = authenticate(username=username, password=password)
        #
        #     if user is not None:
        #         if user.is_active and user.is_manager:
        #             login(request, user)
        #             return redirect('manager_home')
        #         elif user.is_active and user.is_student:
        #             login(request, user)
        #             return redirect('home')
        #         else:
        #             return messages.error(request, 'Enter correct username and password')
        #
        # return render(request, self.template_name, {'form': form}, messages.error(request))

