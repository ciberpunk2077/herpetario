from django import forms
from .base import BaseForm
from apps.catalogo.models import Genero
 
class GeneroForm(BaseForm):
    class Meta:
        model = Genero
        fields = ('familia', 'nombre', 'descripcion') 