from django.urls import path
from passwordManager import views

urlpatterns = [
    # path(route,view,kwargs,name)
    path('save/', views.home, name='pass-manager-page'),
    path('recovery/', views.recovery, name='recovery-page'),
    path('update/', views.update, name='update-page'),
    path('delete/', views.recovery, name='recovery-page'),
]
