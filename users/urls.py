from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup-page'),
    path('signin/', views.signin, name='signin-page'),
    path('', views.signin, name='signin-page'),
    path('signout', views.signout, name='signout-page'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete')
]
