from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Credentials
from .password_ecryptor import *
import xlwt
import xlrd
from datetime import datetime
import pytz
import random


def home(request):
    flag = True
    if request.user.is_authenticated:
        data = {'title': 'PassWord Manager', 'header': 'DASHLINE', 'user': request.user}
        if bool(request.POST):
            if Credentials.objects.filter(website=request.POST.get('site'), login_user=request.user).count() == 0:
                cred = Credentials()
                cred.website = request.POST.get('site')  # fetching site data from request
                cred.username = request.POST.get('text')
                cred.login_user = request.user
                while flag:
                    key = random.randint(100, 999)
                    encrypted_text = text_encryption(plain_text=request.POST.get('password'), salt=key)
                    try:
                        text_decryption(encrypted_text_received=encrypted_text)
                    except:
                        continue
                    else:
                        cred.password = encrypted_text
                        flag = False
                cred.save()
                data.update({'color': '#47d147', 'msg': 'Credentials Saved!'})
                return render(request, 'password_manager.html', {'data': data})
            else:
                data.update({'color': '#ffa31a', 'msg': 'Already Exist!'})
        return render(request, 'password_manager.html', {'data': data})
    else:
        return redirect('signin-page')


def api(request):
    return render(request, 'api.html')


def recovery(request, website=None):
    if request.user.is_authenticated:
        header = 'RECOVERY' if 'delete' not in request.path and 'recover' in request.path else 'DELETE'
        data = {'title': f'PassWord {header.capitalize()}', 'header': header, 'user': request.user, 'website': website}
        if request.POST and request.method == 'POST':
            if check_password(request.POST.get('pass'), request.user.password):
                try:
                    cred = Credentials.objects.get(website=request.POST.get('site'), login_user=request.user)
                    if header == 'RECOVERY' and header != 'DELETE':
                        password_decrypted = text_decryption(encrypted_text_received=cred.password)
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


def update(request, website=None):
    if request.user.is_authenticated:
        is_done = False
        flag = True
        data = {'title': 'PassWord Update', 'header': 'UPDATE', 'user': request.user, 'website': website}
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
                        while flag:
                            key = random.randint(100, 999)
                            encrypted_text = text_encryption(plain_text=request.POST.get('text'), salt=key)
                            try:
                                text_decryption(encrypted_text_received=encrypted_text)
                            except:
                                continue
                            else:
                                cred.password = encrypted_text
                                flag = False
                        is_done = True
                    if is_done:
                        cred.save()
                        color = '#47d147'
                        msg = f"{request.POST.get('update')} has been updated!"
                    else:
                        color = '#ff3333'
                        msg = 'Please select the option!'
                    data.update({'color': color, 'msg': msg})
                except:
                    data.update({'msg': 'Website not Found!', 'color': '#ff3333'})
                return render(request, 'update.html', {'data': data})
            else:
                messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'update.html', {'data': data})
    else:
        return redirect('signin-page')


def export(request):
    if request.user.is_authenticated:
        rows = Credentials.objects.filter(login_user=request.user).order_by('website')
        if rows:
            response = HttpResponse(content_type='application/ms-excel')
            time_zone = pytz.timezone('Asia/Kolkata')
            today = datetime.now(time_zone)
            time_stamp = today.strftime("%d-%B-%Y--%H-%M")
            file_name = '-'.join((str(request.user), time_stamp))
            response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet('Credentials')
            row_num = 1
            font_style = xlwt.easyxf('font: bold 1, height 240')
            columns = ['Website', 'Username', 'Password']
            for col_num in range(len(columns)):
                worksheet.write(row_num, col_num, columns[col_num], font_style)
                worksheet.col(col_num).width = 8 * 1000
            font_style = xlwt.XFStyle()
            data = rows.values_list('website', 'username', 'password')
            for row in data:
                row = list(row)
                row_num += 1
                row[2] = text_decryption(encrypted_text_received=row[2])
                for col_num in range(len(row)):
                    worksheet.write(row_num, col_num, row[col_num], font_style)
            workbook.save(response)
            return response
        else:
            data = {'title': 'PassWord Manager', 'header': 'DASHLINE', 'user': request.user, 'color': '#ff3333',
                    'msg': 'Nothing to export'}
            return render(request, 'password_manager.html', {'data': data})
    else:
        return redirect('signin-page')


def file_import(request):
    if request.user.is_authenticated:
        flag = True
        data = {'title': 'Import PassWord', 'header': 'Import', 'user': request.user}
        if request.FILES:
            if check_password(request.POST.get('pass'), request.user.password):
                try:
                    file = request.FILES['file']
                    workbook = xlrd.open_workbook(file.name, file_contents=file.read())
                    sheet = workbook.sheets()[0]
                    credential_set = ([sheet.cell(r, c).value for c in range(sheet.ncols)] for r in range(sheet.nrows))
                    for credentialSet in credential_set:
                        if '' not in credentialSet and credentialSet[0].lower() != 'website':
                            if Credentials.objects.filter(website=credentialSet[0], login_user=request.user).count() == 0:
                                cred = Credentials()
                                cred.website = credentialSet[0]
                                cred.username = credentialSet[1]
                                flag = True
                                while flag:
                                    key = random.randint(100, 999)
                                    encrypted_text = text_encryption(plain_text=credentialSet[2], salt=key)
                                    try:
                                        text_decryption(encrypted_text_received=encrypted_text)
                                    except:
                                        continue
                                    else:
                                        cred.password = encrypted_text
                                        flag = False
                                cred.login_user = request.user
                                cred.save()
                except:
                    data.update({'color': '#ff3333', 'msg': 'Not Exported by this App'})
                else:
                    data.update({'color': '#47d147', 'msg': 'Credentials Saved!'})
            else:
                messages.error(request, 'Your Password is Incorrect!')
        return render(request, 'import.html', {'data': data})
    else:
        return redirect('signin-page')


def dashboard(request):
    if request.user.is_authenticated:
        data = {'user': request.user}
        collections = Credentials.objects.filter(login_user=request.user).order_by('website')
        cred_container = [[cred.website, cred.username, text_decryption(encrypted_text_received=cred.password)] for cred in collections]
        if not cred_container:
            cred_container = None
        return render(request, 'dashboard.html', {'cred_container': cred_container, 'data': data})
    else:
        return redirect('signin-page')


def page_not_found_view(request, exception):
    return render(request, '404.html')
