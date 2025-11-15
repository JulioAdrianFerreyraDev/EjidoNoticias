from django.contrib import admin
from .models import Categoria, Tag, Noticia, RedSocial

admin.site.register(Categoria)
admin.site.register(Tag)
admin.site.register(Noticia)
admin.site.register(RedSocial)
