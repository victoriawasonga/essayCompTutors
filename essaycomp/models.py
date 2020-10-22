import os
from django.db import models
from django.conf import settings


def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'images')

# Create your models here.
class Order(models.Model):
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    price=models.DecimalField(max_digits=19, decimal_places=2)
    ACADEMICS=(
        ('highschool','High School'),
        ('undergraduate','Undergraduate'),
        ('masters','Masters'),
        ('doctrate','Doctrate'),
    )
    academic_level = models.CharField(max_length=50,choices=ACADEMICS,null=True)
    PAPER=(
        ('custom_essay','Custom Essay'),
        ('research_paper','Research Paper'),
        ('presentation','Presentation'),
        ('thesis','Thesis'),
        ('doctrate','Doctrate'),
    )
    type_of_paper = models.CharField(max_length=50,choices=PAPER,null=True)
    topic=models.CharField(max_length=500,null=True)
    instructions= models.CharField(max_length=500,null=True)
    attachements=models.FilePathField(path=images_path,null=True)
    REF_STYLE=(
        ('apa','APA'),
        ('mla','MLA'),
        ('chicago','Chicago'),
        ('others','Others'),
    )
    reference = models.CharField(max_length=50, choices=REF_STYLE,null=True)
    DEADLINES=(
        ('1wk','1 Week'),
        ('3days','3 Days'),
        ('1day','1 Day'),
        ('24hours','24 Hours'),
        ('12hours','12 hours'),
    )
    deadline = models.CharField(max_length=50, choices=DEADLINES,null=True)
    sources=models.IntegerField(default=1)
    pages=models.IntegerField(default=1)
    SPACE=(
        ('single','Single'),
        ('double','Double '),
    )
    spacing = models.CharField(max_length=50,choices=SPACE,null=True)
    PAYMENT=(
        ('paid','Paid'),
        ('pending','Pending'),
    )
    payment_status = models.CharField(max_length=50,choices=PAYMENT,null=True,default='pending')
    def __str__(self):
        return self.topic

    class Meta:
        orderning:['-date']

class PaidOrders(models.Model):
    order=models.ForeignKey(Order,max_length=200, blank=True, on_delete=models.SET_NULL,null=True)
    created=models.DateTimeField(auto_now_add=True)
    PROGRESS=(
        ('recieved','Recieved'),
        ('ongoing','ongoing'),
        ('done','Done'),
    )
    order_progress = models.CharField(max_length=50,choices=PROGRESS,null=True,default='recieved')

    def __str__(self):
        pass
    class Meta:
        orderning:['-date']


