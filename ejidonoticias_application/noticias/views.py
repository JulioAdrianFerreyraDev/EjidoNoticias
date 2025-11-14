from typing import Any, List
from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Noticia, Categoria



def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().order_by('-id')[:15]
    mas_vistos = Noticia.objects.all().order_by('-vistas')
    
    categorias = Categoria.objects.all()[:7]
    
    context = {
        'noticias': noticias,
        'noticia_mas_vista': mas_vistos[0],
        "noticias_populares": mas_vistos[1:5],
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

def noticias(request) -> HttpResponse:
    noticias_list = Noticia.objects.all().order_by('-id')
    paginator = Paginator(noticias_list, 10)  # Show 10 noticias per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, template_name='screens/noticias.html', context=context)