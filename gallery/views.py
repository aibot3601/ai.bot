from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect

# Create your views here.

def upload_image(request, redir):
    
    if request.method == 'GET':
                
        html_temp = 'upload_image.html'
    
        url = request.path.split('/')        
        
        context = {}
        context['redir'] = url[-1] 
                
        return render(request, 'upload_image.html', {'pagina':context})
        
    elif request.method == 'POST':
        #print(f'{request.POST}, {request.FILES}')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = Image(  image = form.cleaned_data["image"],
                                name = form.cleaned_data["name"]
                                )
            new_image.save()
            return redirect(request.POST.get("redir"))
            
def image_gallery(request):
    images = Image.objects.all()
    return render(request, 'image_gallery.html', {'images': images})
