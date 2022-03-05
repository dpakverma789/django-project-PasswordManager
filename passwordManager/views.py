from django.shortcuts import render, redirect
from passwordManager.models import Credentials
from django.contrib.auth.models import User
from users import urls, views
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .password_ecryptor import pass_encrypt, pass_decrypt

def home(request):
    if request.user.is_authenticated:
        data = {'title': 'PassWord Manager', 'header': 'DASHLINE', 'user': request.user}
        if bool(request.POST):
            if Credentials.objects.filter(website=request.POST.get('site'), login_user=request.user).count() == 0:
                cred = Credentials()
                cred.website = request.POST.get('site')  # fetching site data from request
                cred.username = request.POST.get('text')
                cred.login_user = request.user
                cred.password = pass_encrypt(request.POST.get('password'))
                cred.save()  # saving cred data into database
                data.update({'color': '#47d147', 'msg': 'Credentials Saved!'})
                return render(request, 'password_manager.html', {'data': data})
            else:
                data.update({'color': '#ffa31a', 'msg': 'Already Exist!'})
        return render(request, 'password_manager.html', {'data': data})
    else:
        return redirect('signin-page')


def recovery(request):
    if request.user.is_authenticated:
        header = 'RECOVERY' if 'delete' not in request.path and 'recover' in request.path else 'DELETE'
        data = {'title': f'PassWord {header.capitalize()}', 'header': header, 'user': request.user}
        if request.POST and request.method == 'POST':
            if check_password(request.POST.get('pass'), request.user.password):
                try:
                    cred = Credentials.objects.get(website=request.POST.get('site'), login_user=request.user)
                    if header == 'RECOVERY' and header != 'DELETE':
                        password_decrypted = pass_decrypt(cred.password)
                        data = {'website': cred.website, 'username': cred.username,
                                'password': password_decrypted, 'title': 'PassWord Manager',
                                'header': 'DASHLINE', 'user': request.user}
                        return render(request, 'password_manager.html', {'data': data})
                    else:
                        cred.delete()
                        data.update({'color': '#9933ff', 'msg': 'Credentials Removed!'})
                except:
                    data.update({'msg': 'Website not Found!', 'color': '#ff3333'})
                    return render(request, 'recover.html', {'data': data})
            else:
                messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'recover.html', {'data': data})
    else:
        return redirect('signin-page')


def update(request):
    if request.user.is_authenticated:
        is_done = False
        data = {'title': 'PassWord Update', 'header': 'UPDATE', 'user': request.user}
        if request.POST and request.method == 'POST':
            if check_password(request.POST.get('pass'), request.user.password):
                try:
                    cred = Credentials.objects.get(website=request.POST.get('site'), login_user=request.user)
                    if request.POST.get('update') == 'website':
                        cred.website = request.POST.get('text')
                        is_done = True
                    if request.POST.get('update') == 'username':
                        cred.username = request.POST.get('text')
                        is_done = True
                    if request.POST.get('update') == 'password':
                        cred.password = pass_encrypt(request.POST.get('text'))
                        is_done = True
                    if is_done:
                        cred.save()
                        color = '#47d147'
                        msg = f"{request.POST.get('update')} has been updated!"
                    else:
                        color = '#ff3333'
                    data.update({'color': color, 'msg': request.POST.get('update')})
                except:
                    data.update({'msg': 'Website not Found!', 'color': '#ff3333'})
                return render(request, 'update.html', {'data': data})
            else:
                messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'update.html', {'data': data})
    else:
        return redirect('signin-page')

    