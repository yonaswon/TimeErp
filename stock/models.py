# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone

# User = get_user_model()


# class Stock(models.Model):
#     label_text = models.CharField(max_length=225)
#     Admin = models.ForeignKey(User,on_delete=models.PROTECT)
#     type = models.CharField(max_length=1,choices=(('SA','SUPERADMIN'),
#                                                   ('SM','STOCK MANAGER'),
#                                                   ('PS','PERSONAL STOCK')))
    
#     date = models.DateTimeField(default=timezone.now)


# class Material(models.Model):
#     name = models.CharField(max_length=225,unique=True)
#     type = models.CharField(max_length=1,choices=(('L','length'),
#                                                   ('A','Areal'),
#                                                   ('P','Piece')))

# class LandPMaterialRecored(models.Model):
#     stock = models.ForeignKey(Stock,on_delete=models.PROTECT)
#     material  = models.ForeignKey(Material,on_delete=models.PROTECT)
#     first_amount = models.FloatField()
#     is_available = models.BooleanField(default=True)
#     current_amount = models.FloatField()
#     is_deleted = models.BooleanField(default=False)
#     confirmed = models.BooleanField(default=False)
#     date = models.DateTimeField(default=timezone.now)

# class TransferHistoryForLengthMaterial(models.Model):
#     material = models.ForeignKey(Material,on_delete=models.PROTECT)
   
#     from_stock = models.ForeignKey(Stock, related_name='length_transfers_from', on_delete=models.PROTECT)
#     to_stock = models.ForeignKey(Stock, related_name='length_transfers_to', on_delete=models.PROTECT)
#     amount = models.FloatField()
#     landp = models.ManyToManyField(LandPMaterialRecored)
#     confirmed = models.BooleanField(default=False)
#     date = models.DateTimeField(default=timezone.now)

# class EachArealMaterialRecored(models.Model):
#     stock = models.ForeignKey(Stock,on_delete=models.CharField)
#     material = models.ForeignKey(Material,on_delete=models.PROTECT)
#     code = models.AutoField(primary_key=True)
#     full_width = models.FloatField()
#     full_height = models.FloatField()
#     current_width = models.FloatField()
#     current_height = models.FloatField()
#     estimated_height = models.FloatField()
#     estimated_height = models.FloatField()
#     started = models.BooleanField(default=False)
#     finished = models.BooleanField(default=False)
#     group_id = models.IntegerField(null=True,blank=True)
#     confirmed = models.BooleanField(default=True)
#     date = models.DateTimeField(default=timezone.now)

# class ArealMaterialTransferHistory(models.Model):
#     each_material = models.ForeignKey(EachArealMaterialRecored,on_delete=models.PROTECT)
#     from_stock = models.ForeignKey(Stock, related_name='length_transfers_from', on_delete=models.PROTECT)
#     to_stock = models.ForeignKey(Stock, related_name='length_transfers_to', on_delete=models.PROTECT)

#     width_at_transfer = models.FloatField()
#     hieght_at_transfer = models.FloatField()
#     is_full_at_transfer = models.BooleanField(default=False)
#     confirmed = models.BooleanField(default=False)
#     date  = models.DateTimeField(default=timezone.now)

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Stock(models.Model):
    TYPE_CHOICES = [
        ('SA', 'Super Admin'),
        ('SM', 'Stock Manager'),
        ('PS', 'Personal Stock'),
    ]
    label_text = models.CharField(max_length=225)
    admin = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label_text


class Material(models.Model):
    TYPE_CHOICES = [
        ('L', 'Length'),
        ('A', 'Areal'),
        ('P', 'Piece'),
    ]
    name = models.CharField(max_length=225, unique=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class BaseMaterialRecord(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, db_index=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, db_index=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class LengthMaterialRecord(BaseMaterialRecord):
    first_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)


class ArealMaterialRecord(BaseMaterialRecord):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_width = models.DecimalField(max_digits=8, decimal_places=2)
    full_height = models.DecimalField(max_digits=8, decimal_places=2)
    current_width = models.DecimalField(max_digits=8, decimal_places=2)
    current_height = models.DecimalField(max_digits=8, decimal_places=2)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)


class BaseTransfer(models.Model):
    from_stock = models.ForeignKey(Stock, related_name='transfers_from', on_delete=models.PROTECT)
    to_stock = models.ForeignKey(Stock, related_name='transfers_to', on_delete=models.PROTECT)
    confirmed = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class LengthTransfer(BaseTransfer):
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    records = models.ManyToManyField(LengthMaterialRecord)


class ArealTransfer(BaseTransfer):
    each_material = models.ForeignKey(ArealMaterialRecord, on_delete=models.PROTECT)
    width_at_transfer = models.DecimalField(max_digits=8, decimal_places=2)
    height_at_transfer = models.DecimalField(max_digits=8, decimal_places=2)
    is_full_at_transfer = models.BooleanField(default=False)
