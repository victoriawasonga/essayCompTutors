from django.shortcuts import render

# Create your views here.from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from .models import CustomUser
#get the current url
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.db import models

from django.contrib.auth.decorators import login_required

#rest password 
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')

    def post (self,request):
        context={
            'data':request.POST,
            'has_error':False,
        }
        email=request.POST['email'].lower()
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        username=request.POST.get('username')
        full_name=request.POST.get('name')
        if len(password)<6:
            messages.add_message(request,messages.ERROR,'Passwords should have atleast 6 characters')
            context['has_error']=True
        if password !=  password2:
            messages.add_message(request,messages.ERROR,'Passwords Do not match')
            context['has_error']=True
        if not validate_email(email):
            messages.add_message(request,messages.ERROR,'Please Provide a valid email')
            context['has_error']=True
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request,messages.ERROR,'The email provided is in use***********************')
            context['has_error']=True
        if CustomUser.objects.filter(username=username).exists():
            messages.add_message(request,messages.ERROR,'The Username provided is in use')
            context['has_error']=True
        if context['has_error']:
            return render(request,'authentication/register.html',context)
        else:
            user=CustomUser.objects.create_user(username=username,email=email)
            user.set_password(password)
            user.first_name=full_name
            user.last_name=full_name
            user.is_active=False
            user.save()
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            domain=get_current_site(request).domain
            link=reverse('activate',kwargs={'uidb64':uidb64,'token':generate_token.make_token(user)})
            activate_url='http://'+domain+link
            email_subject="Activate your account"
            email_body='Hi '+user.email+ ' Please use this link to verify your account\n'+activate_url  
            email = EmailMessage(
                email_subject,
                email_body,
                'victoriawasonga@gmail.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.add_message(request,messages.SUCCESS,'Account created successfully')
            return redirect('login')

class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not generate_token.check_token(user, token):
                messages.add_message(request,messages.WARNING,'User already activated')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.add_message(request,messages.SUCCESS,'Acount activated successfully')
            return redirect('login')

        except Exception as ex:
            pass
        return render( request,'authentication/activate_failed.html',status=401)

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        email=request.POST['email'].lower()
        password = request.POST['password']

        if email and password:
            user = auth.authenticate(email=CustomUser.objects.get(email=email), password=password)
            #user=CustomUser.objects.get(email=email)
            print(user)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('profile')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


@login_required(login_url='/authentication/login')
def profileView(request):
     if request.method=='GET':
        return render(request, 'authentication/profile.html')
     if request.method=='POST':
        email=request.POST['email'].lower()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        user_id=request.user.id
        context={
            'data':request.POST,
            'has_error':False,
        }
        if not validate_email(email):
            messages.add_message(request,messages.ERROR,'Please Provide a valid email')
            context['has_error']=True
        if context['has_error']:
            return render(request,'authentication/profile.html',context)
        else:
            t = CustomUser.objects.get(id=user_id)
            t.email= email
            t.first_name= first_name
            t.last_name=last_name
            t.username=username
            t.save()
            messages.add_message(request,messages.SUCCESS,'Acount Updated successfully')
            return redirect('profile')

@login_required(login_url='/authentication/login')
def changePasswordView(request):
     if request.method=='GET':
        return render(request, 'authentication/change_password.html')
     if request.method=='POST':
        context={
             'has_error':False
         }
        password=request.POST.get('password')
        password2=request.POST.get('confirm_password')
        if len(password)<6:
            messages.add_message(request,messages.ERROR,'Passwords should have atleast 6 characters')
            context['has_error']=True
        if password !=  password2:
            messages.add_message(request,messages.ERROR,'Passwords Do not match')
            context['has_error']=True
        if context['has_error']==True:
            return render(request,'authentication/set_new_password.html',context) 
        user_id=request.user.id
        new_user = CustomUser.objects.get(id=user_id)
        new_user.set_password(password)
        new_user.save()
        auth.logout(request)
        messages.add_message(request,messages.SUCCESS,'Password Updated successfully')
        return redirect('profile')
        

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request,'authentication/forgot_password.html')
    def post(self, request):

        email=request.POST['email'].lower()
        if not validate_email(email):
            messages.error(request,'Please enter a valid email')
            return render(request,'authentication/forgot_password.html')
        user=CustomUser.objects.filter(email=email)
        print(user)
        if user.exists():
            email_subject="Reset your account"
            current_site=get_current_site(request)
            message=render_to_string('authentication/reset_user_password.html',
                                     {
                                         'domain':current_site.domain,
                                         'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                                         'token':PasswordResetTokenGenerator().make_token(user[0])
                                     }
            )
           
            email1 = EmailMessage(
                email_subject,
                message,
                'noreply@essaycomptutors.com',
                [email],
            )
            email1.send(fail_silently=False)
            messages.success(request,'We have sent you an email with instruction on how to reset your account')
            return render(request,'authentication/forgot_password.html') 
        else:
            messages.info(request,'no account exist with such an email address')
            return render(request,'authentication/forgot_password.html') 

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request, 'Password reset link is invalid please request a new one ')
                return render(request,'authentication/forgot_password.html') 
            return render(request,'authentication/set_new_password.html',context) 
        except DjangoUnicodeDecodeError as identifier:
            messages.info(request,"Invalid Link")
            return render(request,'authentication/set_new_password.html') 

        return render(request,'authentication/set_new_password.html',context)

        return render(request,'authentication/set_new_password.html',context) 
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token,
            'has_error':False
        }
        password=request.POST.get('password')
        password2=request.POST.get('confirm_password')
        if len(password)<6:
            messages.add_message(request,messages.ERROR,'Passwords should have atleast 6 characters')
            context['has_error']=True
        if password !=  password2:
            messages.add_message(request,messages.ERROR,'Passwords Do not match')
            context['has_error']=True
        if context['has_error']==True:
            return render(request,'authentication/set_new_password.html',context) 
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset success, you can login with the new password ')
            return redirect('login')
            
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something went wrong")
            return render(request,'authentication/set_new_password.html',context) 
            
        

        return render(request,'authentication/set_new_password.html',context)   