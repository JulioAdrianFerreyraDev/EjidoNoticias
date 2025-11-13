from typing import Any, List
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Noticia



def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().order_by('-id')[:5]
    
    return render(request, template_name='index.html', context={'content': noticias, "page_title": 'Inicio'})

def blog(request, slug:str) -> HttpResponse:
    blog = get_object_or_404(Noticia, slug=slug)
    if blog is None:
        return redirect(to='not_found')
        
    blog.vistas += 1
    blog.save()
    return render(request, template_name='screens/blog.html', context={'blog': blog})


def not_found(request) -> HttpResponse:
    return render(request, template_name='screens/404.html', context={})
# Create your views here.
