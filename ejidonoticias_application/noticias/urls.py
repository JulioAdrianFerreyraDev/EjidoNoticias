from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns: list[URLPattern] = [
    path(route='', view=views.index, name='index'),
    path(route='blog/<str:slug>/', view=views.blog, name='blog'),
    path(route='404/', view=views.not_found, name='not_found'),
    
]
