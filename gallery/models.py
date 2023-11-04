from django.db import models

# Create your models here.

class Image(models.Model):
   image = models.ImageField(upload_to = 'gallery')
   name = models.CharField(max_length=200)
