
from django import forms
from django.forms import ModelForm
from .models import Task, Contacto

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

class ContacForm(ModelForm):
    
    rif = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "RIF",
                "class": "form-control",
                'id': "rif"
            }
        ))
    
    nomorg = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Cooperativa",
                "class": "form-control",
                'id': "nomorg"
            }
        ))
        
    correo = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@example.com",
                "class": "form-control",
                'id': "correo"
            }
        ))
        
    mensaje = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Mensaje",
                "class": "form-control",
                'id': "mensaje",
                'rows': "5"
            }
        ))

    class Meta:
        model = Contacto
        fields = ('rif', 'nomorg', 'correo', 'mensaje')
        
