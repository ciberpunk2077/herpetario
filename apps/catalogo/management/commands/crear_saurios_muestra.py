import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.catalogo.models import Familia, Genero, Especie

class Command(BaseCommand):
    help = 'Crea 10 registros de saurios con datos realistas e imágenes locales'

    def handle(self, *args, **options):
        # Eliminar registros previos de Saurio
        self.stdout.write('Eliminando registros previos de Saurio...')
        Especie.objects.filter(tipo_animal='Saurio').delete()
        Genero.objects.filter(familia__nombre__in=[
            'Iguanidae', 'Gekkonidae', 'Scincidae', 'Teiidae', 'Varanidae'
        ]).delete()
        Familia.objects.filter(nombre__in=[
            'Iguanidae', 'Gekkonidae', 'Scincidae', 'Teiidae', 'Varanidae'
        ]).delete()
        self.stdout.write('Registros previos eliminados.')

        familias_saurios = [
            ('Iguanidae', 'Iguanas'),
            ('Gekkonidae', 'Geckos'),
            ('Scincidae', 'Escíncidos'),
            ('Teiidae', 'Lagartos corredores'),
            ('Varanidae', 'Varanos'),
        ]
        generos_saurios = {
            'Iguanidae': [
                ('Iguana', 'Iguanas verdes'),
                ('Ctenosaura', 'Iguanas espinosas'),
            ],
            'Gekkonidae': [
                ('Hemidactylus', 'Geckos caseros'),
                ('Gekko', 'Geckos asiáticos'),
            ],
            'Scincidae': [
                ('Scincus', 'Escíncidos del desierto'),
                ('Eumeces', 'Escíncidos americanos'),
            ],
            'Teiidae': [
                ('Ameiva', 'Lagartos corredores'),
                ('Tupinambis', 'Tegus'),
            ],
            'Varanidae': [
                ('Varanus', 'Varanos'),
            ],
        }
        especies_saurios = {
            'Iguana': ['iguana', 'delicatissima'],
            'Ctenosaura': ['pectinata', 'similis'],
            'Hemidactylus': ['frenatus', 'turcicus'],
            'Gekko': ['gecko', 'smithii'],
            'Scincus': ['scincus', 'officinalis'],
            'Eumeces': ['schneideri', 'algeriensis'],
            'Ameiva': ['ameiva', 'undulata'],
            'Tupinambis': ['merianae', 'rufescens'],
            'Varanus': ['niloticus', 'komodoensis'],
        }
        subtipos_saurios = [
            'Arborícola', 'Terrestre', 'Fosorial', 'Semiacuático', 'No venenoso', 'Defensivo', 'Críptico'
        ]
        habitats_saurios = [
            'Selva tropical', 'Bosque seco', 'Desierto', 'Sabana', 'Matorral', 'Bosque templado', 'Rocas y acantilados', 'Manglares', 'Islas costeras', 'Cuevas'
        ]
        descripciones_saurios = [
            "Saurio de tamaño mediano, adaptado a ambientes cálidos y secos. Presenta escamas brillantes y cola larga.",
            "Lagarto arborícola con dedos prensiles y coloración verde intensa. Excelente trepador y cazador de insectos.",
            "Saurio terrestre de hábitos diurnos, se alimenta principalmente de insectos y pequeños vertebrados.",
            "Lagarto corredor, muy rápido y ágil, habita zonas abiertas y soleadas.",
            "Saurio con capacidad de autotomía caudal, puede desprender su cola para escapar de depredadores.",
            "Lagarto de gran tamaño, depredador oportunista, con fuerte mordida y comportamiento territorial.",
            "Saurio con escamas lisas y cuerpo alargado, adaptado a excavar en suelos arenosos.",
            "Lagarto de hábitos nocturnos, excelente camuflaje y visión adaptada a poca luz.",
            "Saurio con colores llamativos, utilizado en exhibiciones de cortejo y defensa.",
            "Lagarto de importancia ecológica, controla poblaciones de insectos y pequeños roedores."
        ]
        nombres_comunes_saurios = [
            'Iguana verde', 'Gecko casero', 'Lagarto corredor', 'Tegu', 'Varano del Nilo',
            'Iguana espinosa', 'Escíncido del desierto', 'Gecko asiático', 'Lagarto de roca', 'Varano de Komodo'
        ]
        # Crear familias si no existen
        familias_creadas = {}
        for nombre_familia, desc_familia in familias_saurios:
            familia, created = Familia.objects.get_or_create(
                nombre=nombre_familia,
                defaults={'descripcion': desc_familia}
            )
            familias_creadas[nombre_familia] = familia
            if created:
                self.stdout.write(f'Familia creada: {nombre_familia}')
        # Crear géneros si no existen
        generos_creados = {}
        for nombre_familia, generos in generos_saurios.items():
            familia = familias_creadas[nombre_familia]
            for nombre_genero, desc_genero in generos:
                genero, created = Genero.objects.get_or_create(
                    nombre=nombre_genero,
                    familia=familia,
                    defaults={'descripcion': desc_genero}
                )
                generos_creados[nombre_genero] = genero
                if created:
                    self.stdout.write(f'Género creado: {nombre_genero}')
        # Obtener lista de imágenes locales (puedes usar las de anfibios para demo)
        ruta_imagenes = os.path.join('static', 'assets', 'anfibios_muestra')
        imagenes_locales = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        if not imagenes_locales:
            self.stdout.write(self.style.ERROR('No se encontraron imágenes en static/assets/anfibios_muestra/'))
            return
        # Crear especies de saurios
        for i in range(10):
            nombre_familia = random.choice(list(generos_saurios.keys()))
            familia = familias_creadas[nombre_familia]
            nombre_genero = random.choice(generos_saurios[nombre_familia])[0]
            genero = generos_creados[nombre_genero]
            if nombre_genero in especies_saurios:
                nombre_especie = random.choice(especies_saurios[nombre_genero])
            else:
                nombre_especie = f"sp{i+1}"
            if Especie.objects.filter(genero=genero, nombre_especie=nombre_especie).exists():
                nombre_especie = f"{nombre_especie}_{i+1}"
            especie = Especie.objects.create(
                genero=genero,
                nombre_especie=nombre_especie,
                nombre_comun=random.choice(nombres_comunes_saurios),
                tipo_animal='Saurio',
                subtipo=random.choice(subtipos_saurios),
                habitat=random.choice(habitats_saurios),
                descripcion=random.choice(descripciones_saurios),
                peligro_extincion=random.choice([True, False, False, False])
            )
            imagen_path = random.choice(imagenes_locales)
            with open(imagen_path, 'rb') as img_file:
                especie.imagen.save(
                    f'saurio_{especie.id}.jpg',
                    File(img_file),
                    save=True
                )
        self.stdout.write(self.style.SUCCESS('¡Completado! Se crearon 10 especies de saurios con imágenes locales.')) 