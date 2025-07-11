from django import forms

from .base import BaseForm
from apps.catalogo.models import Especie

class SerpientesForm(BaseForm):

    class Meta:
        model = Especie
        fields = (
            'genero', 'nombre_especie', 'nombre_comun', 'tipo_animal', 'subtipo', 
            'habitat', 'peligro_extincion'
        )

class SerpientesUpdateForm(BaseForm):

    class Meta:
        model = Especie
        fields = (
            'genero', 'nombre_especie', 'nombre_comun', 'tipo_animal', 'subtipo', 
            'habitat', 'peligro_extincion'
        )