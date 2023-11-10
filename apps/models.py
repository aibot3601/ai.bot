

from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizacion = models.IntegerField(blank=True, null=True)   
    tip_user = models.IntegerField(blank=True, null=True)
# Create your models here.
