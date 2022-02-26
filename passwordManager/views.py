from django.shortcuts import render, redirect
from passwordManager.models import Credentials
from django.contrib.auth.models import User
from users import urls, views
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


def home(request):
    if request.user.is_authenticated:
        data = {'title': 'PassWord Manager',
                'header': 'DASHLINE',
                'user': request.user if request.user else 'Guest'}
        if bool(request.POST):
            if Credentials.objects.filter(website=request.POST.get('site')).count() == 0:
                cred = Credentials()
                cred.website = request.POST.get('site')  # fetching site data from request
                cred.username = request.POST.get('text')
                cred.password = request.POST.get('password')
                cred.save()  # saving cred data into database
                data.update({'flag': 'success',  'msg': 'Credentials Saved!'})
                return render(request, 'password_manager.html', {'data': data})
            else:
                data.update({'flag': 'exist', 'msg': 'Already Exist!'})
        return render(request, 'password_manager.html', {'data': data})
    else:
        return redirect('signin-page')


def recovery(request):
    if request.user.is_authenticated:
        data = {'title': 'PassWord Recovery', 'header': 'RECOVERY',
                'user': request.user if request.user else 'Guest'}
        if request.POST and request.method == 'POST':
            if check_password(request.POST.get('pass'), request.user.password):
                try:
                    cred = Credentials.objects.get(website=request.POST.get('site'))
                    data = {'website': cred.website, 'username': cred.username,
                            'password': cred.password, 'title': 'PassWord Manager',
                            'header': 'DASHLINE', 'user': request.user if request.user else 'Guest'}
                except:
                    data.update({'flag': 'failed', 'msg': 'Not Found!'})
                    return render(request, 'recover.html', {'data': data})
                return render(request, 'password_manager.html', {'data': data})
            messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'recover.html', {'data': data})
    else:
        return redirect('signin-page')