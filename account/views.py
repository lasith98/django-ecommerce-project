from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from account.forms import LoginForm, SignUpForm


def logout_view(request):
    logout(request)
    return redirect('store:index')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                    pass
                return redirect('account:index')
    else:
        form = LoginForm()
    return render(request, 'account/login-register.html', context={'login_form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.email = username
            user.profile.display_name = username.split("@")[0]
            user.save()
            try:
                group = Group.objects.get(name="Customer")
                user.groups.add(group)
            except Group.DoesNotExist:
                pass
            login(request, user)
            return redirect('account:index')
    else:
        form = SignUpForm()
    return render(request, 'account/login-register.html', {'form': form})


class AccountIndexView(TemplateView):
    template_name = 'account/my-account.html'
