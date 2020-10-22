from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Order,PaidOrders
from django.shortcuts import render

# Create your views here.from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
#get the current url
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError

from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.db import models
from django.contrib.auth import authenticate, login, logout
from authentication.models import CustomUser
import json
from django.http import JsonResponse
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
    if request.method=="GET":
        return render(request,'essaycomp/contact.html')
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        sendit=send_mail(
            subject,
            message, 
            email,
            ['noreply@essaycomptutors.com'])
        sendit.send(fail_silently=False)
        messages.add_message(request,messages.SUCCESS,'Account created successfully')
        return redirect('contactus')

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
def order(request):
    context={
        'values':request.POST,
        'has_error':False
        }
    if request.method=="GET":
        return render(request,'essaycomp/order.html',context)
    if request.method=="POST":
        price=request.POST.get('price')
        academic_level=request.POST.get('academic_level')
        type_of_paper=request.POST.get('type_of_paper')
        topic=request.POST.get('topic')
        instructions=request.POST.get('instructions')
        attachements=request.POST.get('attachements')
        reference=request.POST.get('reference')
        deadline=request.POST.get('deadline')
        sources=request.POST.get('sources')
        pages=request.POST.get('pages')
        spacing=request.POST.get('spacing')
    
        user_id=request.user
        if request.user.is_authenticated:
            Order.objects.create(user_id=user_id,price=price,academic_level=academic_level,type_of_paper=type_of_paper,topic=topic,instructions=instructions,attachements=attachements,reference=reference,deadline=deadline
                ,sources=sources,pages=pages,spacing=spacing)
            messages.success(request,'Order Details captured correctly')
            return redirect('view_orders')
        
        else:
            messages.error(request,'User is not logged in')
            return redirect('login')
    
def ViewOrders(request):
    if request.method=="GET":
        order=Order.objects.filter(user_id_id=request.user,payment_status='pending')
        context={
            'orders':order
        }
        return render(request,'essaycomp/view_order.html',context)
    if request.method=="POST":
        pass
def order_view(request,id):
    order=Order.objects.get(pk=id)
    context={
        'order':order,
        'values':order,
    }
    if request.method=="GET":
        
        return render(request,'essaycomp/order_detail.html',context)
    else:
        messages.info(request,'Handling Post form')

        return render(request,'essaycomp/order_detail.html',context)
def order_edit(request,id):
    order=Order.objects.get(pk=id)
    context={
        'order':order,
        'values':order,
    }
    if request.method=="GET":
        
        return render(request,'essaycomp/order_edit.html',context)
    if request.method=="POST":
        price=request.POST.get('price')
        academic_level=request.POST.get('academic_level')
        type_of_paper=request.POST.get('type_of_paper')
        topic=request.POST.get('topic')
        instructions=request.POST.get('instructions')
        attachements=request.POST.get('attachements')
        reference=request.POST.get('reference')
        deadline=request.POST.get('deadline')
        sources=request.POST.get('sources')
        pages=request.POST.get('pages')
        spacing=request.POST.get('spacing')
        if sources=="":
            sources=0
        if pages=="":
            pages=0
    
        user_id=request.user
        if request.user.is_authenticated:
            order.user_id=user_id
            order.price=price
            order.academic_level=academic_level
            order.type_of_paper=type_of_paper
            order.topic=topic
            order.instructions=instructions
            order.attachements=attachements
            order.reference=reference
            order.deadline=deadline
            order.sources=sources
            order.pages=pages
            order.spacing=spacing
            order.save()
            messages.success(request,'Order Details updated correctly')
            return redirect('view_orders')
        
        else:
            messages.error(request,'User is not logged in')
            return redirect('login')


def order_payment(request,id):
    order=Order.objects.get(pk=id)
    context={
        'order':order,
    }
    if request.method=="GET":
        return render(request,'essaycomp/order_payment.html',context)

def paymentComplete(request):
    body=json.loads(request.body)
    print('BODY',body)
    id=body['order_id']
    complete_order=Order.objects.get(pk=id)
    complete_order.payment_status='paid'
    complete_order.save()
    PaidOrders.objects.create(
        order=complete_order
    )
    return JsonResponse('Payment completed!',safe=False)
def ViewPayments(request):
    if request.method=="GET":
        order=Order.objects.filter(user_id_id=request.user,payment_status='paid')
        
        context={
            'orders':order
        }
        return render(request,'essaycomp/view_payment.html',context)
    if request.method=="POST":
        pass


def payment_details(request,id):
    order=Order.objects.get(pk=id)
    payments=PaidOrders.objects.get(order=id)
    context={
        'order':order,
        'payments':payments,

    }
    if request.method=="GET":
        
        return render(request,'essaycomp/payment_detail.html',context)
    else:
        messages.info(request,'Handling Post form')