from django import forms

from .base import BaseForm
from apps.catalogo.models import Serpientes

class SerpientesForm(BaseForm):

    class Meta:
        model = Serpientes
        fields = (
            'nombre_comun', 'nombre_cientifico', 'area_distribucion', 'categoria_riesgo', 'dieta', 'orden',
            'suborden', 'nombre_del_cientifico', 'especie', 'descripcion', 'imagen', 'referencia_bibliografica'
        )

class SerpientesUpdateForm(BaseForm):

    class Meta:
        model = Serpientes
        fields = (
            'nombre_comun', 'nombre_cientifico', 'area_distribucion', 'categoria_riesgo', 'dieta', 'orden',
            'suborden', 'nombre_del_cientifico', 'especie', 'descripcion', 'imagen', 'referencia_bibliografica'
        )