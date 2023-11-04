from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect

# Create your views here.

def upload_image(request):
    if request.method == 'GET':
        return render(request, 'upload_image.html')
    elif request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = Image(  image = form.cleaned_data["image"],
                                name = form.cleaned_data["name"]
                                )
            new_image.save()
            return HttpResponseRedirect('/gallery/image_gallery/')
            
def image_gallery(request):
    images = Image.objects.all()
    print(images)
    return render(request, 'image_gallery.html', {'images': images})
