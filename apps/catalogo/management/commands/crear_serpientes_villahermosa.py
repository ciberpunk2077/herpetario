import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.catalogo.models import Familia, Genero, Especie

class Command(BaseCommand):
    help = 'Crea 1000 registros de serpientes de la región de Villahermosa, Tabasco, México'

    def handle(self, *args, **options):
        # Eliminar géneros y familias específicas de serpientes antes de crear nuevos
        generos_a_eliminar = [
            'Bothrops', 'Agkistrodon', 'Crotalus', 'Porthidium', 'Leptodeira', 'Drymobius', 'Coniophanes',
            'Thamnophis', 'Imantodes', 'Ninia', 'Lampropeltis', 'Oxybelis', 'Mastigodryas', 'Tantilla',
            'Geophis', 'Micrurus', 'Boa', 'Corallus'
        ]
        familias_a_eliminar = ['Viperidae', 'Colubridae', 'Elapidae', 'Boidae']
        Genero.objects.filter(nombre__in=generos_a_eliminar).delete()
        Familia.objects.filter(nombre__in=familias_a_eliminar).delete()
        
        # Familias de serpientes de la región
        familias_serpientes = [
            ('Viperidae', 'Víboras - Serpientes venenosas de colmillos móviles'),
            ('Colubridae', 'Culebras - Familia más diversa, mayoría no venenosas'),
            ('Elapidae', 'Coralillos - Serpientes venenosas de colmillos fijos'),
            ('Boidae', 'Boas - Serpientes constrictoras'),
        ]

        # Géneros comunes de la región
        generos_serpientes = {
            'Viperidae': [
                ('Bothrops', 'Nauyaca'),
                ('Agkistrodon', 'Cantiles'),
                ('Crotalus', 'Cascabeles'),
                ('Porthidium', 'Mano de metate'),
            ],
            'Colubridae': [
                ('Leptodeira', 'Falsas nauyacas'),
                ('Drymobius', 'Culebras corredoras'),
                ('Coniophanes', 'Culebras de tierra'),
                ('Thamnophis', 'Culebras de agua'),
                ('Imantodes', 'Serpientes liana'),
                ('Ninia', 'Culebras pequeñas'),
                ('Lampropeltis', 'Falsas corales'),
                ('Oxybelis', 'Bejuquillas'),
                ('Mastigodryas', 'Culebras corredoras'),
                ('Tantilla', 'Culebras diminutas'),
                ('Geophis', 'Culebras de tierra'),
            ],
            'Elapidae': [
                ('Micrurus', 'Coralillos verdaderos'),
            ],
            'Boidae': [
                ('Boa', 'Boa constrictora'),
                ('Corallus', 'Boas arborícolas'),
            ],
        }

        especies_serpientes = {
            'Bothrops': ['asper', 'nummifer'],
            'Agkistrodon': ['bilineatus', 'taylori'],
            'Crotalus': ['simus', 'tzabcan'],
            'Porthidium': ['nasutum', 'ophryomegas'],
            'Leptodeira': ['annulata', 'septentrionalis', 'bakeri'],
            'Drymobius': ['margaritiferus', 'multicinctus', 'chloroticus'],
            'Coniophanes': ['imperialis', 'piceivittis', 'quinquivittatus'],
            'Thamnophis': ['sirtalis', 'proximus', 'marcianus'],
            'Imantodes': ['cenchoa', 'gemmistratus', 'inornatus'],
            'Ninia': ['atrata', 'diademata', 'sebae'],
            'Lampropeltis': ['polyzona'],
            'Oxybelis': ['aeneus', 'brevirostris'],
            'Mastigodryas': ['boddaerti', 'cliftoni', 'melanolomus'],
            'Tantilla': ['calamarina', 'melanocephala', 'rubra'],
            'Geophis': ['dubius', 'ruthveni', 'semidoliatus'],
            'Micrurus': ['diastema', 'elegans', 'limbatus', 'nigrocinctus', 'alleni', 'fulvius'],
            'Boa': ['constrictor'],
            'Corallus': ['hortulanus', 'annulatus'],
        }

        subtipos_serpientes = [
            'Venenosa', 'No venenosa', 'Constrictora', 'Arborícola', 'Terrestre', 'Acuática', 'Fosorial', 'Diurna', 'Nocturna', 'Defensiva', 'Críptica'
        ]

        habitats_serpientes = [
            'Selva tropical', 'Bosque de galería', 'Manglares', 'Sabana', 'Bosque secundario', 'Zonas urbanas', 'Ríos y lagunas', 'Rocas y acantilados', 'Cuevas', 'Áreas de cultivo', 'Pastizales', 'Riberas de ríos', 'Islas fluviales', 'Áreas pantanosas', 'Bosque de tular', 'Zonas de transición'
        ]

        descripciones_serpientes = [
            "Serpiente común de la región de Villahermosa, adaptada a ambientes húmedos y cálidos. Presenta patrones de coloración variables y hábitos principalmente nocturnos.",
            "Serpiente venenosa de importancia médica, reconocida por su cabeza triangular y colmillos móviles.",
            "Serpiente arborícola que habita en la vegetación densa de la selva tabasqueña. Excelente trepadora y cazadora de pequeños vertebrados.",
            "Serpiente acuática que frecuenta ríos y lagunas de la región. Se alimenta principalmente de peces y anfibios.",
            "Serpiente fosorial que excava madrigueras en suelos húmedos. Presenta cuerpo alargado y escamas lisas.",
            "Serpiente de hábitos diurnos, activa durante el día en busca de presas pequeñas.",
            "Serpiente críptica que se camufla entre la hojarasca y vegetación del bosque tropical.",
            "Serpiente defensiva que emite sonidos o adopta posturas amenazantes cuando se siente en peligro.",
            "Serpiente de importancia ecológica en el control de poblaciones de roedores y anfibios en los ecosistemas de Tabasco.",
            "Serpiente adaptada a las condiciones urbanas de Villahermosa, frecuentemente observada en jardines y parques."
        ]

        nombres_comunes_serpientes = [
            'Nauyaca', 'Cantil', 'Cascabel', 'Mano de metate', 'Falsa nauyaca', 'Culebra corredora', 'Culebra de tierra', 'Culebra de agua', 'Serpiente liana', 'Culebra pequeña', 'Falsa coral', 'Bejuquilla', 'Culebra diminuta', 'Boa constrictora', 'Coralillo', 'Boa arborícola', 'Serpiente de río', 'Serpiente de manglar', 'Serpiente de sabana', 'Serpiente de cueva', 'Serpiente urbana', 'Serpiente de acantilado', 'Serpiente de transición', 'Serpiente de pastizal', 'Serpiente de tular', 'Serpiente de isla', 'Serpiente de galería', 'Serpiente de roca', 'Serpiente de cultivo', 'Serpiente de pantano', 'Serpiente de bosque'
        ]

        # Crear familias
        familias_creadas = {}
        for nombre_familia, desc_familia in familias_serpientes:
            familia, created = Familia.objects.get_or_create(
                nombre=nombre_familia,
                defaults={'descripcion': desc_familia}
            )
            familias_creadas[nombre_familia] = familia
            if created:
                self.stdout.write(f'Familia creada: {nombre_familia}')

        # Crear géneros
        generos_creados = {}
        for nombre_familia, generos in generos_serpientes.items():
            if nombre_familia in familias_creadas:
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

        # Usar imágenes de muestra
        ruta_imagenes = os.path.join('static', 'assets', 'serpientes_villahermosa')
        imagenes_disponibles = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        if not imagenes_disponibles:
            self.stdout.write(self.style.ERROR('No se encontraron imágenes en static/assets/serpientes_villahermosa/'))
            return

        # Crear 1000 especies de serpientes
        especies_creadas = 0
        for i in range(1000):
            nombre_familia = random.choice(list(generos_serpientes.keys()))
            if nombre_familia in familias_creadas:
                familia = familias_creadas[nombre_familia]
                generos_disponibles = generos_serpientes[nombre_familia]
                nombre_genero, desc_genero = random.choice(generos_disponibles)
                if nombre_genero in generos_creados:
                    genero = generos_creados[nombre_genero]
                    if nombre_genero in especies_serpientes:
                        nombre_especie = random.choice(especies_serpientes[nombre_genero])
                    else:
                        nombre_especie = f"sp{i+1}"
                    if Especie.objects.filter(genero=genero, nombre_especie=nombre_especie).exists():
                        nombre_especie = f"{nombre_especie}_{i+1}"
                    especie = Especie.objects.create(
                        genero=genero,
                        nombre_especie=nombre_especie,
                        nombre_comun=random.choice(nombres_comunes_serpientes),
                        tipo_animal='Serpiente',
                        subtipo=random.choice(subtipos_serpientes),
                        habitat=random.choice(habitats_serpientes),
                        descripcion=random.choice(descripciones_serpientes),
                        peligro_extincion=random.choice([True, False, False, False, False])
                    )
                    imagen_path = random.choice(imagenes_disponibles)
                    try:
                        with open(imagen_path, 'rb') as img_file:
                            especie.imagen.save(
                                f'serpiente_villahermosa_{especie.id}.jpg',
                                File(img_file),
                                save=True
                            )
                        especies_creadas += 1
                        if especies_creadas % 100 == 0:
                            self.stdout.write(f'Progreso: {especies_creadas} especies creadas...')
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error al asignar imagen a especie {especie.id}: {e}'))
                        especies_creadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'¡Completado! Se crearon {especies_creadas} especies de serpientes de Villahermosa, Tabasco, México.'
            )
        ) 