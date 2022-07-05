from django.urls import path
from passwordManager import views

urlpatterns = [
    # path(route,view,kwargs,name)
    path('save/', views.home, name='pass-manager-page'),
    path('recovery/', views.recovery, name='recovery-page'),
    path('update/', views.update, name='update-page'),
    path('delete/', views.recovery, name='recovery-page'),
    path('export/', views.export, name='export-page'),
    path('import/', views.file_import, name='import-page'),
]

handler404 = "passwordManager.views.page_not_found_view"