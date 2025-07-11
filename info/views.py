from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from apps.catalogo.models import Especie, Familia

class HomeViews(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeViews, self).get_context_data(**kwargs)
        search=self.request.GET.get('search')
        if search:
            serpientes = Especie.objects.filter(
                Q(nombre_comun__icontains=search) | 
                Q(nombre_especie__icontains=search) |
                Q(genero__nombre__icontains=search),
                tipo_animal='Serpiente'
            )
            especies = Especie.objects.filter(
                Q(nombre_comun__icontains=search) | 
                Q(nombre_especie__icontains=search) |
                Q(genero__nombre__icontains=search)
            )
            familias = Familia.objects.filter(
                Q(nombre__icontains=search) | 
                Q(descripcion__icontains=search)
            )
            context['search'] = True
            context['serpientes'] = serpientes
            context['especies'] = especies
            context['familias'] = familias

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

def presentacion(request):
    return render(request, 'presentacion.html')

def coleccion(request):
    return render(request, 'coleccion.html')

def investigacion(request):
    return render(request, 'investigacion.html')

def personal(request):
    return render(request, 'personal.html')
