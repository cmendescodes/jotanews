from django.contrib import admin
from .models import Noticia, Categoria, Subcategoria, Tag

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao', 'urgente', 'categoria', 'subcategoria', 'fonte')
    list_filter = ('categoria', 'subcategoria', 'urgente')
    search_fields = ('titulo', 'conteudo')
