from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username

class Contacto(models.Model):
  rif = models.CharField(max_length=20)
  nomorg = models.CharField(max_length=100)
  correo = models.CharField(max_length=100)
  mensaje = models.TextField(max_length=1000)

  def __str__(self):
    return self.nomorg
    
class Image(models.Model):
    title = models.CharField(max_length=128)
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title}"
