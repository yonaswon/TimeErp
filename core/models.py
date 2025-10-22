from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class TeamRole(models.Model):
    Name = models.CharField(max_length=225)
    date = models.DateTimeField(default=timezone.now)

class User(AbstractUser):
    telegram_id = models.IntegerField()
    role = models.ManyToManyField(TeamRole,blank=True)
    telegram_user_name = models.CharField(max_length=225,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

