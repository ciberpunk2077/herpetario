from django.core.management.base import BaseCommand
from apps.catalogo.models import Familia, Genero, Especie


class Command(BaseCommand):
    help = 'Crea datos de prueba para el catálogo de especies'

    def handle(self, *args, **options):
        # Crear familias
        familia_viperidae = Familia.objects.create(
            nombre="Viperidae",
            descripcion="Familia de serpientes venenosas que incluye víboras y crótalos"
        )
        
        familia_colubridae = Familia.objects.create(
            nombre="Colubridae",
            descripcion="Familia de serpientes no venenosas más grande del mundo"
        )

        # Crear géneros
        genero_crotalus = Genero.objects.create(
            nombre="Crotalus",
            familia=familia_viperidae,
            descripcion="Género de serpientes cascabel"
        )
        
        genero_bothrops = Genero.objects.create(
            nombre="Bothrops",
            familia=familia_viperidae,
            descripcion="Género de víboras americanas"
        )
        
        genero_lampropeltis = Genero.objects.create(
            nombre="Lampropeltis",
            familia=familia_colubridae,
            descripcion="Género de serpientes rey"
        )

        # Crear especies
        Especie.objects.create(
            genero=genero_crotalus,
            nombre_especie="durissus",
            nombre_comun="Cascabel tropical",
            tipo_animal="Serpiente",
            subtipo="Venenosa",
            habitat="Bosques tropicales y sabanas",
            peligro_extincion=False
        )
        
        Especie.objects.create(
            genero=genero_bothrops,
            nombre_especie="asper",
            nombre_comun="Terciopelo",
            tipo_animal="Serpiente",
            subtipo="Venenosa",
            habitat="Bosques húmedos tropicales",
            peligro_extincion=False
        )
        
        Especie.objects.create(
            genero=genero_lampropeltis,
            nombre_especie="triangulum",
            nombre_comun="Serpiente rey",
            tipo_animal="Serpiente",
            subtipo="Constrictora",
            habitat="Bosques y praderas",
            peligro_extincion=False
        )

        self.stdout.write(
            self.style.SUCCESS('Datos de prueba creados exitosamente')
        ) 