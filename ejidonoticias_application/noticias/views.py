from typing import Any, List
from django.shortcuts import render
from django.http import HttpResponse
from .models import Noticia

blogs : List[dict[str,Any]] = [
    {"title": "Esta es mi casa",
        "author": "Me mismo",
        "date": "Hoy",
        "reading_time": "5 minutos",
        "views": 1000,
        "category": "Villa",
        "tags": ["hogar", "familia", "comodidad"],
        "slug": "villa-casa",
        "banner_image_url": "https://placehold.co/1920x927?text=Villa+Casa",},
    {
        "title": "Esta es mi casa 2",
        "author": "Me mismo",
        "date": "Hoy",
        "reading_time": "5 minutos",
        "views": 2500,
        "category": "Mundo",
        "tags": ["hogar", "familia", "comodidad"],
        "slug": "villa-hogar",
        "banner_image_url": "https://placehold.co/1920x927?text=Hello+World",
    }
]


def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().order_by('-id')[:5]
    
    return render(request, template_name='index.html', context={'content': noticias, "page_title": 'Inicio'})

def blog(request, slug:str) -> HttpResponse:
    blog = Noticia.objects.get(slug=slug)
    blog.vistas += 1
    blog.save()
    return render(request, template_name='screens/blog.html', context={'blog': blog})

# Create your views here.
