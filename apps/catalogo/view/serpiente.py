from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView

from apps.catalogo.forms.serpiente import SerpientesForm, SerpientesUpdateForm
from apps.catalogo.models import Serpientes


class SerpientesListView(ListView):
    model = Serpientes

    def get_queryset(self):
        return Serpientes.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SerpientesListView, self).get_context_data(**kwargs)
        return context


class SerpientesCreateView(CreateView):
    model = Serpientes
    form_class = SerpientesForm

    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.save()
        messages.success(self.request, "El registro ha sido creadao con éxito.")
        return super(SerpientesCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(SerpientesCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalogo:serpiente-list')


class SerpientesUpdateView(UpdateView):
    model = Serpientes
    form_class = SerpientesUpdateForm

    def get_context_data(self, **kwargs):
        context = super(SerpientesUpdateView, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def form_valid(self, form):
        form.instance.user_by = self.request.user.pk
        form.instance.updated_at = now()
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
        context['serpiete'] = Serpientes.objects.get(pk=pk_serpiente)
        return context

class SerpientesDeleteView(DeleteView):
    model = Serpientes

    def get_success_url(self):
        messages.success(self.request, "El registro ha sido eliminado con éxito.")
        return reverse_lazy('catalogo:serpiente-list')
