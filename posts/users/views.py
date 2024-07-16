from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginUserForm, RegistrationUserForm
from .models import MyUser


class Login(FormView):
    template_name = 'authorization/login.html'
    form_class = LoginUserForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(self.request, username=data['email'], password=data['password'])
        if user is not None:
            login(self.request, user)
            return redirect(reverse_lazy('home'))
        messages.error(self.request, 'Your email or password is invalid')
        return redirect(reverse_lazy('login'))


class Registration(FormView):
    template_name = 'authorization/registration.html'
    form_class = RegistrationUserForm

    def form_valid(self, form):
        data = form.cleaned_data
        if data['password1'] != data['password2']:
            messages.error(self.request, 'Passwords are not the same')
            return redirect(reverse_lazy('registration'))
        if MyUser.objects.filter(email=data['email']).exists():
            messages.error(self.request, 'User with this email already exists')
            return redirect(reverse_lazy('login'))
        MyUser.objects.create_user(email=data['email'], password=data['password1'], date_of_birth='2222-12-22')
        return redirect(reverse_lazy('home'))


def log_out(request):
    logout(request)
    return redirect(reverse_lazy('login'))