from django import forms

from .base import BaseForm
from apps.catalogo.models import Especie, Genero, Familia

class AnfibiosForm(BaseForm):
    familia = forms.ModelChoiceField(queryset=Familia.objects.all(), required=True, label='Familia')
    especie = forms.ModelChoiceField(queryset=Especie.objects.none(), required=False, label='Especie')
    SUBTIPO_CHOICES = [
        ('', '---------'),
        ('Venenoso', 'Venenoso'),
        ('No venenoso', 'No venenoso'),
        ('Tóxico', 'Tóxico'),
    ]
    subtipo = forms.ChoiceField(choices=SUBTIPO_CHOICES, required=False, label='Subtipo')

    class Meta:
        model = Especie
        fields = (
            'familia',
            'genero',
            'especie',
            'nombre_comun',
            'subtipo',
            'habitat',
            'descripcion',
            'peligro_extincion',
            'imagen',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'familia' in self.data:
            try:
                familia_id = int(self.data.get('familia'))
                self.fields['genero'].queryset = Genero.objects.filter(familia_id=familia_id)
            except (ValueError, TypeError):
                self.fields['genero'].queryset = Genero.objects.none()
        elif self.instance.pk:
            self.fields['genero'].queryset = Genero.objects.filter(familia=self.instance.genero.familia)
            self.fields['familia'].initial = self.instance.genero.familia
        else:
            self.fields['genero'].queryset = Genero.objects.none()

        if 'genero' in self.data:
            try:
                genero_id = int(self.data.get('genero'))
                self.fields['especie'].queryset = Especie.objects.filter(genero_id=genero_id)
            except (ValueError, TypeError):
                self.fields['especie'].queryset = Especie.objects.none()
        elif self.instance.pk:
            self.fields['especie'].queryset = Especie.objects.filter(genero=self.instance.genero)
            self.fields['especie'].initial = self.instance.pk
        else:
            self.fields['especie'].queryset = Especie.objects.none()

        # Aplicar estilos a campos específicos
        self.fields['nombre_comun'].widget.attrs['class'] = self.fields['nombre_comun'].widget.attrs.get('class', '') + ' bg-blue-100'
        self.fields['habitat'].widget.attrs['class'] = self.fields['habitat'].widget.attrs.get('class', '') + ' bg-blue-100'
        
        # Configurar el campo descripción como textarea grande
        if 'descripcion' in self.fields:
            self.fields['descripcion'].widget = forms.Textarea(attrs={
                'class': 'form-input w-full px-4 py-3 rounded-lg bg-blue-100 h-32 resize-y',
                'placeholder': 'Describe las características, comportamiento, hábitos y otros detalles importantes de la especie...',
                'style': 'min-height: 128px;'
            })

    def clean(self):
        cleaned_data = super().clean()
        genero = cleaned_data.get('genero')
        familia = cleaned_data.get('familia')
        especie = cleaned_data.get('especie')
        if genero and familia and genero.familia != familia:
            self.add_error('genero', 'El género seleccionado no pertenece a la familia elegida.')
        if especie and especie.genero != genero:
            self.add_error('especie', 'La especie seleccionada no pertenece al género elegido.')
        return cleaned_data

class AnfibiosUpdateForm(AnfibiosForm):
    pass 