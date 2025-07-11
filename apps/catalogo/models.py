from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de Usuario personalizado
class User(AbstractUser):
    administrador = models.BooleanField(default=False)
    capturista = models.BooleanField(default=False)
    usuario = models.BooleanField(default=False)

# Taxonomía
class Familia(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ej: "Viperidae"
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ej: "Crotalus"
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='generos')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.familia.nombre})"

# Modelo principal corregido (una sola clase Especie)
class Especie(models.Model):
    TIPO_ANIMAL_CHOICES = [
        ('Serpiente', 'Serpiente'),
        ('Anfibio', 'Anfibio'),
        ('Saurio', 'Saurio'),
    ]

    # Relaciones taxonómicas (en lugar de campos CharField)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name='especies')
    nombre_especie = models.CharField(max_length=50)  # Parte específica del nombre científico
    nombre_comun = models.CharField(max_length=100, blank=True)
    
    # Clasificación general
    tipo_animal = models.CharField(max_length=20, choices=TIPO_ANIMAL_CHOICES)
    subtipo = models.CharField(max_length=50, blank=True)  # Ej: "Venenosa", "Constrictora"
    habitat = models.CharField(max_length=100, blank=True)
    peligro_extincion = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Especies"
        unique_together = [('genero', 'nombre_especie')]  # Evita duplicados científicos

    def __str__(self):
        return f"{self.nombre_cientifico} ({self.nombre_comun})"

    @property
    def nombre_cientifico(self):
        return f"{self.genero.nombre} {self.nombre_especie}"

    @property
    def familia(self):
        return self.genero.familia.nombre  # Acceso directo a la familia

# Atributos dinámicos
class AtributoEspecie(models.Model):
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, related_name='atributos')
    clave = models.CharField(max_length=50)  # Ej: "tipo_veneno", "humedad_ideal"
    valor = models.TextField()

    def __str__(self):
        return f"{self.clave}: {self.valor} (para {self.especie.nombre_cientifico})"