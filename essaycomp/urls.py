from django.conf.urls import url
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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

]


urlpatterns+=staticfiles_urlpatterns()