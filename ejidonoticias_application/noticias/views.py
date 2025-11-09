from typing import Any, List
from django.shortcuts import render
from django.http import HttpResponse
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
    content : dict = {
        "title": "Esta es mi casa",
        "author": "Me mismo",
        "date": "Hoy",
        "reading_time": "5 minutos",
        "views": 1000,
        "category": "Villa",
        "tags": ["hogar", "familia", "comodidad"],
        "content": "lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "slug": "villa-casa",
        "banner_image_url": "https://placehold.co/1920x927?text=Hello+World",
    }
    return render(request, template_name='index.html', context={'content': content, "page_title": 'Inicio'})

def blog(request, slug:str) -> HttpResponse:
    blog : dict[str, Any] | None = next((b for b in blogs if b['slug'] == slug), None)
    return render(request, template_name='screens/blog.html', context={'blog': blog})

# Create your views here.
