from django.db import models
from stock.models import Material
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class EachPurcheseMaterial(models.Model):
    material = models.ForeignKey(Material,on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    date = models.DateTimeField(default=timezone.now)


class Purchese(models.Model):
    created_by  = models.ForeignKey(User,on_delete=models.CASCADE)
    each_material_purchese = models.ManyToManyField(EachPurcheseMaterial)
    status = models.CharField(max_length=2,choices=(('P','IN PROGRESS'),
                                                    ('D','DONE PURCHESED')))
    payed_from = models.CharField(max_length=1,choices=(('F','FINANCE'),
                                                        ('A','ADMIN')))
    request_status = models.CharField(max_length=2,choices=(('NS','NOT SENT'),
                                                            ('S','SENT'),
                                                            ('C','CONFIRMED')))
    payment_screenshot = models.ImageField(upload_to='/paymentscreenshoot',null=True,blank=True)

    payment_code = models.CharField()
    is_delete = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)



