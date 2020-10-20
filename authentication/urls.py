from django.urls import path
from. import views
from django.conf.urls import url
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('register',views.RegistrationView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>',views.ActivateAccount.as_view(),name='activate'),
    path('profile', profileView, name='profile'),
    path('request_reset_link',RequestPasswordResetEmail.as_view(),name="request_reset_link"),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
    path('change_password', changePasswordView, name='change_password'),


]
