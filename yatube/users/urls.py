from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import path
from . import views


app_name = 'users'
password_change = 'users/password_change.html'
password_change_ok = 'users/password_change_done.html'
password_reset_fm = 'users/password_reset_form.html'
password_reset_ok = 'users/password_reset_done.html'
password_reset_conf = 'users/password_reset_confirm.html'
password_reset_com = 'users/password_reset_complite.html'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name=password_change),
        name='password_change'),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name=password_change_ok),
        name='password_change_done'),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name=password_reset_fm),
        name='password_reset_form'),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name=password_reset_ok),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name=password_reset_conf),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name=password_reset_com),
        name='password_reset_complete'), ]
