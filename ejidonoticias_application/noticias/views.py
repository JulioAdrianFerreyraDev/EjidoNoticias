from typing import Any, List
from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Noticia, Categoria



def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().order_by('-id')[:15]
    mas_visto = Noticia.objects.all().order_by('-vistas').first()
    
    categorias = Categoria.objects.all()[:7]
    
    context = {
        'noticias': noticias,
        'mas_visto': mas_visto,
        'categorias': categorias,
    }
    
    template = 'index.html'
    
    return render(request, template_name=template, context=context)
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
