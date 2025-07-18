from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET

from apps.catalogo.forms.familia import FamiliaForm, FamiliaUpdateForm
from apps.catalogo.models import Familia, Genero
from apps.catalogo.forms.genero import GeneroForm


class FamiliaListView(ListView):
    model = Familia

    def get_queryset(self):
        return Familia.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FamiliaListView, self).get_context_data(**kwargs)
        return context


class FamiliaCreateView(CreateView):
    mo6del = Familia
    form_class = FamiliaForm

    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.save()
        messages.success(self.request, "El registro ha sido creado con exito.")
        return super(FamiliaListView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(FamiliaCreateView, self).form_invalid(form)

    def get_success_url(self):
            return reverse_lazy('catalogo:familia-list')


class FamiliaUpdateView(UpdateView):
    model = Familia
    form_class = FamiliaUpdateForm

    def get_context_data(self, **kwargs):
        context = super(FamiliaUpdateView, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.instance.updated_at = now()
        form.save()
        messages.success(self.request, "El registro ha sido actualizado con éxito.")
        return super(FamiliaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(FamiliaUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:familia-list')


class FamiliaDeleteView(DeleteView):
    model = Familia

    def get_success_url(self):
        messages.success(self.request, "El registro ha sido eliminado con éxito.")
        return reverse_lazy('catalogo:familia-list')


@csrf_exempt
@require_POST
def crear_familia_ajax(request):
    form = FamiliaForm(request.POST)
    if form.is_valid():
        familia = form.save()
        return JsonResponse({
            'success': True,
            'id': familia.id,
            'nombre': familia.nombre
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


@require_GET
def generos_por_familia_ajax(request):
    familia_id = request.GET.get('familia_id')
    generos = []
    if familia_id:
        generos = Genero.objects.filter(familia_id=familia_id).values('id', 'nombre')
    return JsonResponse({'generos': list(generos)})


@csrf_exempt
@require_POST
def crear_genero_ajax(request):
    form = GeneroForm(request.POST)
    if form.is_valid():
        genero = form.save()
        return JsonResponse({
            'success': True,
            'id': genero.id,
            'nombre': genero.nombre
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
