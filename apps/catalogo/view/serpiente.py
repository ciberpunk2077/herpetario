from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.catalogo.forms.serpiente import SerpientesForm, SerpientesUpdateForm
from apps.catalogo.models import Especie, Genero


class SerpientesListView(ListView):
    model = Especie
    template_name = 'catalogo/serpiente_list.html'

    def get_queryset(self):
        return Especie.objects.filter(tipo_animal='Serpiente')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerpientesListView, self).get_context_data(**kwargs)
        return context


class SerpientesCreateView(CreateView):
    model = Especie
    form_class = SerpientesForm
    template_name = 'catalogo/serpiente_form.html'

    def form_valid(self, form):
        form.instance.tipo_animal = 'Serpiente'
        form.save()
        messages.success(self.request, "El registro ha sido creado con éxito.")
        return super(SerpientesCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(SerpientesCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:serpiente-list')


class SerpientesUpdateView(UpdateView):
    model = Especie
    form_class = SerpientesUpdateForm
    template_name = 'catalogo/serpiente_form.html'

    def get_context_data(self, **kwargs):
        context = super(SerpientesUpdateView, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def form_valid(self, form):
        form.instance.tipo_animal = 'Serpiente'
        form.save()
        messages.success(self.request, "El registro ha sido actualizado con éxito.")
        return super(SerpientesUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(SerpientesUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:serpiente-list')

class SerpientesDetailView(TemplateView):
    template_name = 'catalogo/serpiente_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SerpientesDetailView, self).get_context_data(**kwargs)
        pk_serpiente = self.kwargs.get('pk')
        context['serpiente'] = Especie.objects.get(pk=pk_serpiente)
        return context

class SerpientesDeleteView(DeleteView):
    model = Especie

    def get_success_url(self):
        messages.success(self.request, "El registro ha sido eliminado con éxito.")
        return reverse_lazy('catalogo:serpiente-list')

@require_GET
def especie_por_genero_ajax(request):
    genero_id = request.GET.get('genero_id')
    especies = []
    if genero_id:
        especies = Especie.objects.filter(genero_id=genero_id)
    return JsonResponse({'especies': [
        {'id': e.id, 'nombre_cientifico': f'{e.genero.nombre} {e.nombre_especie}'} for e in especies
    ]})

@csrf_exempt
@require_POST
def especie_crear_ajax(request):
    genero_id = request.POST.get('genero')
    nombre_especie = request.POST.get('nombre_especie')
    nombre_comun = request.POST.get('nombre_comun')
    if not (genero_id and nombre_especie):
        return JsonResponse({'success': False, 'errors': 'Datos incompletos'}, status=400)
    try:
        genero = Genero.objects.get(pk=genero_id)
    except Genero.DoesNotExist:
        return JsonResponse({'success': False, 'errors': 'Género no encontrado'}, status=400)
    especie, created = Especie.objects.get_or_create(
        genero=genero,
        nombre_especie=nombre_especie,
        defaults={'nombre_comun': nombre_comun or '', 'tipo_animal': 'Serpiente'}
    )
    return JsonResponse({
        'success': True,
        'id': especie.id,
        'nombre_cientifico': f'{genero.nombre} {especie.nombre_especie}'
    })
