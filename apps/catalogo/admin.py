# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Familia, Genero, Especie, AtributoEspecie

class GeneroInline(admin.TabularInline):
    model = Genero
    extra = 1

class AtributoEspecieInline(admin.TabularInline):
    model = AtributoEspecie
    extra = 1

@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    inlines = [GeneroInline]

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'familia')
    list_filter = ('familia',)

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre_cientifico', 'familia', 'tipo_animal', 'imagen_tag')
    list_filter = ('genero__familia', 'tipo_animal')
    inlines = [AtributoEspecieInline]
    readonly_fields = ('imagen_tag',)
    fields = ('genero', 'nombre_especie', 'nombre_comun', 'tipo_animal', 'subtipo', 'habitat', 'peligro_extincion', 'imagen', 'imagen_tag')

    def imagen_tag(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_tag.short_description = 'Imagen'