from typing import Any, List
from django.shortcuts import render
from django.http import HttpResponse
from .models import Noticia



def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().order_by('-id')[:5]
    
    return render(request, template_name='index.html', context={'content': noticias, "page_title": 'Inicio'})

def blog(request, slug:str) -> HttpResponse:
    blog = Noticia.objects.get(slug=slug)
    blog.vistas += 1
    blog.save()
    return render(request, template_name='screens/blog.html', context={'blog': blog})

# Create your views here.
