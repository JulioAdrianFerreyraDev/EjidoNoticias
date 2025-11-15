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
    
    # 1. Obtener todos los parámetros
    query = request.GET.get('q')
    category_query = request.GET.get('category')
    tag_query = request.GET.get('tag')

    # 2. Empezar con un queryset base que incluya todo
    # Usamos .filter() en lugar de .all() para una mejor optimización
    # y filtramos solo las noticias publicadas (¡buena práctica!)
    noticias_list = Noticia.objects.filter(publicado=True)

    # 3. Aplicar filtros EN CADENA (AND)
    if query:
        # Filtra el queryset existente
        noticias_list = noticias_list.filter(titulo__icontains=query)
    
    if category_query:
        # Filtra el queryset existente
        noticias_list = noticias_list.filter(categoria__slug__iexact=category_query)
    
    if tag_query:
        # Filtra el queryset existente
        # ¡Importante! Añadir .distinct() cuando se filtra por ManyToMany
        noticias_list = noticias_list.filter(tags__slug__iexact=tag_query).distinct()

    # 4. Aplicar el orden al final (¡DRY!)
    # Es más común ordenar blogs por fecha que por ID
    noticias_list = noticias_list.order_by('-fecha_publicacion')
    
    # 5. Paginación (tu código era correcto)
    paginator = Paginator(noticias_list, 2)  # 10 noticias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # --- 6. MEJORA CRÍTICA para Paginación ---
    # Prepara los parámetros de la URL para que los enlaces 
    # de paginación no pierdan los filtros.
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    
    # 7. Construir el contexto final
    context = {
        'blogs': page_obj,
        'q': query, # Para mostrar en la barra de búsqueda lo que se buscó
        'category': category_query, # Para saber qué categoría está activa
        'tag': tag_query, # Para saber qué tag está activo
        'query_params': params.urlencode(), # Para los enlaces de paginación
    }
    
    print(noticias_list)  # Depuración: muestra la consulta SQL generada

    return render(request, template_name='screens/blogs.html', context=context)