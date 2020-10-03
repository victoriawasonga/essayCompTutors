from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
def index(request):
    return render(request,'essaycomp/index.html')
def works(request):
    return render(request,'essaycomp/works.html')
def about(request):
    return render(request,'essaycomp/about.html')
def services(request):
    return render(request,'essaycomp/services.html')
def contactus(request):
    return render(request,'essaycomp/contact.html')
    #send mail
    #send_mail(
    #message_name,# subject
    #message   ,# message
    #message_email   ,# from mail 
    #['kachieng98@gmail.com'] ,#  To Email
    #)'''
def order(request):
    return render(request,'essaycomp/order.html')
def revision_policy(request):
    return render(request,'essaycomp/revision_policy.html')
def privacy_policy(request):
    return render(request,'essaycomp/privacy_policy.html')
def terms_of_use(request):
    return render(request,'essaycomp/terms_of_use.html')
def copyright_policy(request):
    return render(request,'essaycomp/copyright_policy.html')
def faq(request):
    return render(request,'essaycomp/faq.html')