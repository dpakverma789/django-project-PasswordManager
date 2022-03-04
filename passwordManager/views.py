from django.shortcuts import render, redirect
from passwordManager.models import Credentials
from django.contrib.auth.models import User
from users import urls, views
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


def pass_encrypt(simple_text, encrypted_password='', key='x'):
    try:
        for i in simple_text:
            if i.isalpha():
                ascii_pass_encrypt = ord(i)
                binary_pass = hex(ascii_pass_encrypt)
            elif i.isnumeric():
                binary_pass = hex(int(i))
            else:
                ascii_pass_encrypt = ord(i)
                binary_pass = hex(ascii_pass_encrypt)
            encrypted_password += binary_pass[2:] + key
    except:
        encrypted_password = simple_text
    finally:
        return encrypted_password


def pass_decrypt(password_Encrypted, key='x'):
    splited_password = password_Encrypted.split(key)[:-1]
    return loopKey(splited_password,password_Encrypted)


def loopKey(splited_password, password_Encrypted, orignal_password=''):
    sample = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-']
    sample2 = ['_', '+', '=', ' ', '[', ']', '{', '}', '"', "'"]
    is_done = False
    for x in splited_password:
        concat_data = int(x, 16)
        flag = chr(int(concat_data))
        if flag.isalpha():
            ascii_pass_decrypt = str(flag)
            orignal_password += ascii_pass_decrypt
        elif flag in sample or flag in sample2:
            ascii_pass_decrypt = str(flag)
            orignal_password += ascii_pass_decrypt
        else:
            orignal_password += str(concat_data)
        is_done = True
    if is_done:
        return orignal_password
    else:
        orignal_password = password_Encrypted
        return orignal_password


def home(request):
    if request.user.is_authenticated:
        data = {'title': 'PassWord Manager',
                'header': 'DASHLINE',
                'user': request.user if request.user else 'Guest'}
        if bool(request.POST):
            if Credentials.objects.filter(website=request.POST.get('site'), login_user=request.user).count() == 0:
                cred = Credentials()
                cred.website = request.POST.get('site')  # fetching site data from request
                cred.username = request.POST.get('text')
                cred.login_user = request.user
                cred.password = pass_encrypt(request.POST.get('password'))
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
                    cred = Credentials.objects.get(website=request.POST.get('site'), login_user=request.user)
                    password_decrypted = pass_decrypt(cred.password)
                    data = {'website': cred.website, 'username': cred.username,
                            'password': password_decrypted, 'title': 'PassWord Manager',
                            'header': 'DASHLINE', 'user': request.user if request.user else 'Guest'}
                except:
                    data.update({'flag': 'failed', 'msg': 'Not Found!'})
                    return render(request, 'recover.html', {'data': data})
                return render(request, 'password_manager.html', {'data': data})
            messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'recover.html', {'data': data})
    else:
        return redirect('signin-page')
    