from django.urls import path
from users import views
from .views import PasswordReset

urlpatterns = [

    path('signup', views.signup, name='signup-page'),
    path('signin', views.signin, name='signin-page'),
    path('', views.signin, name='signin-page'),
    path('signout', views.signout, name='signout-page'),
    path('forgot-password', PasswordReset.as_view(), name='password-reset'),
]
