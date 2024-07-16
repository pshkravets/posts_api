from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from users.models import MyUser
from .forms import ReplyCommentsSettings
from .utils import validate_time


def home(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            return redirect(reverse_lazy('login'))
        context = {}
        context['api_key'] = request.user.jwt_token
        time_dict = validate_time(request.user.reply_delay)
        time_dict['reply_enabled'] = request.user.auto_reply_enabled
        context['form'] = ReplyCommentsSettings(initial=time_dict)
        return render(request, 'home.html', context)
    if request.method == 'POST':
        form = ReplyCommentsSettings(request.POST)
        form.is_valid()
        data = form.cleaned_data
        request.user.auto_reply_enabled = data['reply_enabled']
        request.user.reply_delay = data['reply_hours'] * 3600 + data['reply_minutes'] * 60 + data['reply_seconds']
        request.user.save()
        return redirect(reverse_lazy('home'))