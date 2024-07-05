from django.urls import reverse_lazy
from django.shortcuts import redirect


def home(request):
    if request.user.is_anonymous:
        return redirect(reverse_lazy('login'))