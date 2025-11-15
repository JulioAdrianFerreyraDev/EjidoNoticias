
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Noticia, Categoria
from django.db.models import F



def index(request) -> HttpResponse:
    noticias = Noticia.objects.all().filter(publicado=True).order_by('-id')[:15]
    mas_vistos = Noticia.objects.all().filter(publicado=True).order_by('-vistas')
    
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
    
    blog = get_object_or_404(Noticia, slug=slug, publicado=True)

    noticias_populares = Noticia.objects.filter(publicado=True) \
                                      .exclude(pk=blog.pk) \
                                      .order_by('-vistas')[:5]
    
    noticias_relacionadas = Noticia.objects.filter(
        publicado=True,
        categoria=blog.categoria
    ).exclude(pk=blog.pk).order_by('-fecha_publicacion')[:5]


    categorias = Categoria.objects.all()[:4]
    
    Noticia.objects.filter(slug=slug).update(vistas=F('vistas') + 1)
        
    context = {
        'blog': blog,
        "noticia_mas_popular" : noticias_populares[0] if noticias_populares else None,
        'noticias_populares': noticias_populares[1:],
        'noticias_relacionadas': noticias_relacionadas,
        'categorias': categorias,
        
    }

    return render(request, template_name='screens/blog.html', context=context)


def not_found(request) -> HttpResponse:
    return render(request, template_name='404.html', context={})
# Create your views here.

def noticias(request) -> HttpResponse:
    
    # 1. Obtener todos los parámetros
    query = request.GET.get('q')
    category_query = request.GET.get('category')
    tag_query = request.GET.get('tag')


    noticias_list = Noticia.objects.filter(publicado=True)

    if query:

        noticias_list = noticias_list.filter(titulo__icontains=query)
    
    if category_query:

        noticias_list = noticias_list.filter(categoria__slug__iexact=category_query)
    
    if tag_query:

        noticias_list = noticias_list.filter(tags__slug__iexact=tag_query).distinct()

    noticias_list = noticias_list.order_by('-fecha_publicacion')
    

    paginator = Paginator(noticias_list, 15)  # 10 noticias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    

    context = {
        'blogs': page_obj,
        'q': query, 
        'category': category_query, 
        'tag': tag_query, 
        'query_params': params.urlencode(), 
    }
    
    return render(request, template_name='screens/blogs.html', context=context)