from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import smtplib
import random
from django.core.mail import send_mail
from django.conf import settings

from .models import Task, Contacto

from .forms import TaskForm, ContacForm, SignUpForm, LoginForm

# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": SignUpForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": SignUpForm, "error": "Nombre de Usuario ya existe."})

        return render(request, 'signup.html', {"form": SignUpForm, "error": "Las contraseñas no coinciden."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    return render(request, 'home.html')

def contacto(request):
    if request.method == "GET":
        return render(request, 'contacto.html', {"form": ContacForm})
    else:
        try:
            form = ContacForm(request.POST)
            new_msg = form.save(commit=False)
            new_msg.save()
            
            subject = request.POST['asunto']
            message = request.POST['mensaje'] + " " + request.POST['correo']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['javsalas@gmail.com', 'intalgos@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('home')
        except ValueError:
            return render(request, 'contacto.html', {"form": ContacForm, "error": "Error al enviar formulario de Contacto."})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": LoginForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": LoginForm, "error": "Usuario o contraseña incorrecto."})

        login(request, user)
        return redirect('tasks')
        
def pages(request):
    context = {}
    contextajax = {}
    comi = "'"
    ruta = request.path.split('/')
    
    metodo = request.method
    #['', 'tasks', 'password', 'vertext', '']
        
    if metodo == 'POST':
            
        ruta = request.path.split('/')
                    
        if ruta[-2] == 'vertext':
            
            comi = "'"
                
            arrinptipo = ruta[-3].split('.')
            
            inptipo = arrinptipo[1]
            
            idpassword = arrinptipo[0]
            
            print(request.POST)
            
            print(idpassword)
                
            password = request.POST.get(idpassword)
            
            print(password)
                    
            if inptipo == 'password':
                inptipo = 'text'
                eye = 'fa-solid fa-eye-slash'
                tooltitulo = 'Ocultar Contraseña'
            elif inptipo == 'text':
                inptipo = 'password'
                eye = 'fa-solid fa-eye'
                tooltitulo = 'Mostrar Contraseña'
                
            appurls = ruta[-4]
            
            arrdiv_eye = ruta[-1].split('.') 
            
            frm = arrdiv_eye[0]  
            
            div_eye = arrdiv_eye[1]  
            
            genpw = ''
            
            if frm == 'frmsignup':
                genpw = '<span class="input-group-text btn btn-secondary" id="basic-addon1" style="padding: 15px; font-size: 17px;" data-bs-toggle="tooltip" data-bs-placement="top" title="Generar Contraseña"><i class="fa fa-cog" aria-hidden="true" style="cursor: pointer;" ></i></span>'
            
            span = f'{genpw}<div class="form-floating"><input type="{inptipo}" name="{idpassword}" placeholder="Contraseña" class="form-control" id="{idpassword}" value="{password}" required><label for="{idpassword}">Contraseña</label></div><div class="input-group-prepend"><span class="input-group-text btn btn-secondary" id="basic-addon1" style="padding: 15px; font-size: 17px;" data-bs-toggle="tooltip" data-bs-placement="top" title="{tooltitulo}"><i id="pweye" class="{eye}" style="cursor: pointer;" onclick="mospsw({comi}{inptipo}{comi},{comi}{appurls}{comi},{comi}{frm}{comi},{comi}{div_eye}{comi},{comi}{idpassword}{comi})"></i></span></div>'
                      
            dataobj = {
                 'span': span,
                 'frm': frm,
                 'ruta': ruta[-2]
            }
                
            return JsonResponse({'data': dataobj})
            
        elif ruta[-2] == 'genpassw':

            generated_password = ''
    # generated_password = ''.join([random.choice(
    #     string.ascii_letters + string.digits + string.punctuation) for n in range(12)])

            characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#$%_1234567890')

            for x in range(10):
                generated_password += random.choice(characters)
            
                      
            dataobj = {
                 'valpassw': generated_password,
                 'ruta': ruta[-2]
            }
            
            return JsonResponse({'data': dataobj})
            
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
        
def send_email():
    try:
        username='****'
        password='***'
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
    except Exception as e:
        print(e)
        
'''


'''        
        
        
        
        
