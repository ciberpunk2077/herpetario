from django.db import models

# Create your models here.
import os
from pyexpat import model

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# Usuarios

class User(AbstractUser):
    administrador = models.BooleanField(default=False)
    capturista = models.BooleanField(default=False)
    usuario = models.BooleanField(default=False)

class Familia(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)

    class Meta:
        default_permissions =()

    def __str__(self):
        return f'{self.nombre}'

class Especie(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    familia = models.ForeignKey("catalogo.Familia", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f'{self.nombre}'


class Serpientes(models.Model):
    def get_upload_path_imagen(instance, filename):
        folder = 'imagenes/serpientes/{}/{}/{}'.format(instance.especie.nombre,instance.especie.nombre,instance.get_genero_display())
        ruta = os.path.join("media/",folder)
        return os.path.join(ruta,filename)

    CHOICES_GENERO = ((1, 'Masculino'), (2, 'Femenino'),  (3, 'Hermafrodita'))
    CHOICES_VENENOSA = ((1, 'Si'), (2, 'No'))

    genero = models.IntegerField(choices=CHOICES_GENERO,null=True,blank=True)
    venenosa = models.IntegerField(choices=CHOICES_VENENOSA,null=True,blank=True)
    nombre_comun = models.CharField(max_length=200, null=True, blank=True)
    nombre_cientifico = models.CharField(max_length=200)
    area_distribucion = models.CharField(max_length=500, null=True, blank=True)
    categoria_riesgo = models.CharField(max_length=500, null=True, blank=True)
    dieta = models.CharField(max_length=500, null=True, blank=True)
    orden = models.CharField(max_length=200, null=True, blank=True)
    suborden = models.CharField(max_length=200, null=True, blank=True)
    nombre_del_cientifico = models.CharField(max_length=200, null=True, blank=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    imagen = models.FileField(upload_to=get_upload_path_imagen, null=True, blank=True)
    referencia_bibliografica = models.CharField(max_length=300, null=True, blank=True)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, null=True, blank=False)


    class Meta:
        default_permissions = ()
