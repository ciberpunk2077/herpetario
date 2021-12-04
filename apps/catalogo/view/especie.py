from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.catalogo.forms.especie import EspecieForm, EspecieUpdateForm
from apps.catalogo.models import Especie


class EspecieListView(ListView):
    model = Especie

    def get_queryset(self):
        return Especie.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EspecieListView, self).get_context_data(**kwargs)
        return context


class EspecieCreateView(CreateView):
    model = Especie
    form_class = EspecieForm


    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.save()
        messages.success(self.request, "El registro ha sido creadao con éxito.")
        return super(EspecieCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(EspecieCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:especie-list')


class EspecieUpdateView(UpdateView):
    model = Especie
    form_class = EspecieUpdateForm

    def get_context_data(self, **kwargs):
        context = super(EspecieUpdateView, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.instance.updated_at = now()
        form.save()
        messages.success(self.request, "El registro ha sido actualizado con éxito.")
        return super(EspecieUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(EspecieUpdateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:especie-list')

class EspecieDeleteView(DeleteView):
    model = Especie

    def get_success_url(self):
        messages.success(self.request, "El registro ha sido eliminado con éxito.")
        return reverse_lazy('catalogo:especie-list')