from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class DesignType(models.Model):
    name = models.CharField(max_length=225)

class Order(models.Model):
    posted_by = models.ForeignKey(User,on_delete=models.PROTECT)
    design_type = models.ForeignKey(DesignType,on_delete=models.PROTECT)
    order_code = models.AutoField(primary_key=True)
    client = models.CharField(max_length=225)
    contact   = models.CharField(max_length=13)
    delivery_date = models.DateTimeField()
    location = models.CharField(max_length=225)
    full_payment = models.IntegerField()

    

