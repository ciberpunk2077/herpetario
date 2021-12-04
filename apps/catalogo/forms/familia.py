from django import forms
from .base import  BaseForm
from  apps.catalogo.models import Familia

class FamiliaForm(BaseForm):

    class Meta:
        model = Familia
        fields = ('nombre', 'descripcion')

class FamiliaUpdateForm(BaseForm):

    class Meta:
        model = Familia
        fields = ('nombre', 'descripcion')