from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from passwordManager import urls
# Create your views here.


def signin(request):
    if request.method == 'POST' and request.POST:
        user_username = request.POST.get('username')
        user_master_password = request.POST.get('password')
        if User.objects.filter(username=user_username).count():
            users = authenticate(username=user_username, password=user_master_password)
            if users is not None:
                login(request, users)
                return redirect('pass-manager-page')
            else:
                messages.error(request, 'Your Password is Incorrect!')
        else:
            messages.error(request, 'You are Not a User!')
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST' and request.POST:
        user_email = request.POST.get('email').strip()
        user_first_name = request.POST.get('first_name').strip()
        user_last_name = request.POST.get('last_name').strip()
        user_username = request.POST.get('username').strip()
        user_master_password = request.POST.get('password').strip()
        user_password_confirm = request.POST.get('password_confirm').strip()
        if user_master_password == user_password_confirm:
            if User.objects.filter(username=user_username).count() == 0:
                users = User.objects.create_user(user_username, user_email, user_master_password)
                users.first_name = user_first_name
                users.last_name = user_last_name
                users.save()
                messages.success(request, 'Account successfully created!')
                return redirect('signin-page')
            else:
                messages.error(request, f'Account with \'{user_username}\' already exist')
        else:
            messages.warning(request, 'Confirm Password Didn\'t Matached')
    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('signin-page')