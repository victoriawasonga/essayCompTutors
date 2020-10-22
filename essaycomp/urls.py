from django.conf.urls import url
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^works$', works, name='works'),
    url(r'^about$', about, name='about'),
    url(r'^services$', services, name='services'),
    url(r'^contactus$', contactus, name='contactus'),
    url(r'^order$', order, name='order'),
    url(r'^revision_policy$', revision_policy, name='revision_policy'),
    url(r'^privacy_policy$', privacy_policy, name='privacy_policy'),
    url(r'^terms_of_use$', terms_of_use, name='terms_of_use'),
    url(r'^copyright_policy$', copyright_policy, name='copyright_policy'),
    url(r'^faq$', faq, name='faq'),
    url(r'^view_orders$', ViewOrders, name='view_orders'),
    path('order_view/<int:id>', order_view, name='order_details'),
    path('payment_details/<int:id>', payment_details, name='payment_details'),
    path('order_edit/<int:id>', order_edit, name='order_edit'),
    path('order_payment/<int:id>', order_payment, name='order_payment'),
    path('complete', paymentComplete, name='complete'),
    path('view_payments', ViewPayments, name='view_payments'),

]


urlpatterns+=staticfiles_urlpatterns()