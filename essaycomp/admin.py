from django.contrib import admin
# Register your models here.
from .models import Order
from .models import PaidOrders

admin.site.register(PaidOrders)
admin.site.register(Order)