from django import forms
from  .base import BaseForm
from  apps.catalogo.models import Especie,Familia

class EspecieForm(BaseForm):

    class Meta:
        model = Especie
        fields = ('nombre', 'familia', 'descripcion')

        familia = forms.ChoiceField(label='Familia')

        def __init__(self, *args, **kwargs):
            super(EspecieForm, self).__init__(*args, **kwargs)
            familia = [(inst.id, inst.nombre) for inst in Familia.objects.all()]
            print('familia', familia)
            self.fields['familia'].choices = familia

class EspecieUpdateForm(BaseForm):

    class Meta:
        model = Especie
        fields = ('nombre', 'familia', 'descripcion')

        familia = forms.ChoiceField(label='Familia')

        def __init__(self, *args, **kwargs):
            super(EspecieForm, self).__init__(*args, **kwargs)
            familia = [(inst.id, inst.nombre) for inst in Familia.objects.all()]
            print('familia', familia)
            self.fields['familia'].choices = familia