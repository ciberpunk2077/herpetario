from msilib.schema import ListView

from django.db.models import Q, Count
from django.shortcuts import render

# Create your view here.
from django.views.generic import TemplateView, ListView

from apps.catalogo.models import Especie, Familia, Genero


class HomeViews(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeViews, self).get_context_data(**kwargs)
        
        # Estadísticas del catálogo para la gráfica
        context['total_especies'] = Especie.objects.count()
        context['total_serpientes'] = Especie.objects.filter(tipo_animal='Serpiente').count()
        context['total_anfibios'] = Especie.objects.filter(tipo_animal='Anfibio').count()
        context['total_saurios'] = Especie.objects.filter(tipo_animal='Saurio').count()
        context['total_familias'] = Familia.objects.count()
        context['total_generos'] = Genero.objects.count()
        
        # Calcular porcentajes para las barras de progreso
        if context['total_especies'] > 0:
            context['porcentaje_serpientes'] = (context['total_serpientes'] / context['total_especies']) * 100
            context['porcentaje_anfibios'] = (context['total_anfibios'] / context['total_especies']) * 100
            context['porcentaje_saurios'] = (context['total_saurios'] / context['total_especies']) * 100
        else:
            context['porcentaje_serpientes'] = 0
            context['porcentaje_anfibios'] = 0
            context['porcentaje_saurios'] = 0
        
        # Top 5 familias con más especies
        context['top_familias'] = Familia.objects.annotate(
            num_especies=Count('generos__especies')
        ).order_by('-num_especies')[:5]
        
        # Serpientes por subtipo
        context['serpientes_venenosas'] = Especie.objects.filter(
            tipo_animal='Serpiente', 
            subtipo='Venenosa'
        ).count()
        context['serpientes_no_venenosas'] = Especie.objects.filter(
            tipo_animal='Serpiente', 
            subtipo='No venenosa'
        ).count()
        context['serpientes_constrictoras'] = Especie.objects.filter(
            tipo_animal='Serpiente', 
            subtipo='Constrictora'
        ).count()
        
        # Especies en peligro de extinción por tipo (nombres corregidos)
        context['serpientes_en_peligro_count'] = Especie.objects.filter(
            tipo_animal='Serpiente', 
            peligro_extincion=True
        ).count()
        context['anfibios_en_peligro_count'] = Especie.objects.filter(
            tipo_animal='Anfibio', 
            peligro_extincion=True
        ).count()
        context['saurios_en_peligro_count'] = Especie.objects.filter(
            tipo_animal='Saurio', 
            peligro_extincion=True
        ).count()
        
        # Total de especies en peligro
        context['especies_en_peligro'] = Especie.objects.filter(peligro_extincion=True).count()
        
        return context


class BusquedaView(ListView):
    model = Especie
    template_name = 'catalogo/busqueda.html'
    context_object_name = 'especies'
    paginate_by = 20

    def get_queryset(self):
        queryset = Especie.objects.all()
        q = self.request.GET.get('q')
        
        if q:
            # Buscar en múltiples campos usando Q objects
            queryset = queryset.filter(
                Q(genero__familia__nombre__icontains=q) |  # Familia
                Q(genero__nombre__icontains=q) |           # Género
                Q(nombre_especie__icontains=q) |           # Especie
                Q(nombre_comun__icontains=q) |             # Nombre común
                Q(subtipo__icontains=q)                    # Subtipo
            ).distinct()
        
        return queryset.select_related('genero', 'genero__familia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_resultados'] = self.get_queryset().count()
        return context


class PresentacionView(TemplateView):
    template_name = '../templates/presentacion.html'

    def get_context_data(self, **kwargs):
        context = super(PresentacionView, self).get_context_data(**kwargs)
        return context

class ColeccionView(TemplateView):
    template_name = '../templates/coleccion.html'

    def get_context_data(self, **kwargs):
        context = super(ColeccionView, self).get_context_data(**kwargs)
        return context

class InvestigacionView(TemplateView):
    template_name = '../templates/investigacion.html'

    def get_context_data(self, **kwargs):
        context = super(InvestigacionView, self).get_context_data(**kwargs)
        return context

class PersonalView(TemplateView):
    template_name = '../templates/personal.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalView, self).get_context_data(**kwargs)
        return context

def prueba(request):
    return render(request, 'catalogo/prueba.html')

def serpiente(request):
    return render(request, 'catalogo/serpiente_list.html')


