
from django.shortcuts import render, redirect
from passwordManager.models import Credentials
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .password_ecryptor import pass_encrypt, pass_decrypt
import xlwt
import xlrd


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
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{request.user}.xls"'
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Credentials')
        row_num = 1
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Website', 'Username', 'Password']
        for col_num in range(len(columns)):
            worksheet.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = Credentials.objects.filter(login_user=request.user).order_by('website')
        data = rows.values_list('website', 'username', 'password')
        for row in data:
            row = list(row)
            row_num += 1
            row[2] = pass_decrypt(row[2])
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num], font_style)
        workbook.save(response)
        return response
    else:
        return redirect('signin-page')


def file_import(request):
    if request.user.is_authenticated:
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
                                cred.password = pass_encrypt(credentialSet[2])
                                cred.login_user = request.user
                                cred.save()
                except:
                    data.update({'color': '#ff3333', 'msg': 'Unsupported File Format'})
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
        cred_container = ([cred.website, cred.username, pass_decrypt(cred.password)]
                          for cred in Credentials.objects.filter(login_user=request.user))
        return render(request, 'dashboard.html', {'cred_container': cred_container, 'data': data})
    else:
        return redirect('signin-page')


def page_not_found_view(request, exception):
    return render(request, '404.html')
