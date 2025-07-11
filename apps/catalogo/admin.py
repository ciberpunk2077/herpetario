# admin.py
from django.contrib import admin
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
    list_display = ('nombre_cientifico', 'familia', 'tipo_animal')
    list_filter = ('genero__familia', 'tipo_animal')
    inlines = [AtributoEspecieInline]