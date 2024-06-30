from django.contrib import admin
from passwordManager.models import Credentials
from import_export.admin import ExportActionMixin, ImportMixin


class CredentialsAdmin(ExportActionMixin, ImportMixin, admin.ModelAdmin):
    list_display = ('website', 'username', 'password', 'login_user')


admin.site.register(Credentials, CredentialsAdmin)
