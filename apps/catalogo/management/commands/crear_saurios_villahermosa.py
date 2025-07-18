import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.catalogo.models import Familia, Genero, Especie

class Command(BaseCommand):
    help = 'Crea 350 registros de saurios de la región de Villahermosa, Tabasco, México'

    def handle(self, *args, **options):
        # Eliminar registros previos de Saurio
        self.stdout.write('Eliminando registros previos de Saurio...')
        Especie.objects.filter(tipo_animal='Saurio').delete()
        
        # Eliminar géneros y familias específicas de saurios
        generos_a_eliminar = [
            'Iguana', 'Ctenosaura', 'Hemidactylus', 'Gekko', 'Scincus', 'Eumeces', 
            'Ameiva', 'Tupinambis', 'Varanus', 'Anolis', 'Basiliscus', 'Corytophanes',
            'Norops', 'Sceloporus', 'Urosaurus', 'Uta', 'Phrynosoma', 'Aspidoscelis',
            'Cnemidophorus', 'Holcosus', 'Kentropyx', 'Lepidophyma', 'Xantusia',
            'Coleonyx', 'Phyllodactylus', 'Thecadactylus', 'Gonatodes', 'Sphaerodactylus'
        ]
        
        familias_a_eliminar = [
            'Iguanidae', 'Gekkonidae', 'Scincidae', 'Teiidae', 'Varanidae',
            'Dactyloidae', 'Corytophanidae', 'Phrynosomatidae', 'Xantusiidae'
        ]
        
        Genero.objects.filter(nombre__in=generos_a_eliminar).delete()
        Familia.objects.filter(nombre__in=familias_a_eliminar).delete()
        
        self.stdout.write('Registros previos eliminados.')

        # Familias de saurios de Villahermosa, Tabasco
        familias_saurios = [
            ('Iguanidae', 'Iguanas - Familia de lagartos grandes y robustos'),
            ('Dactyloidae', 'Anolis - Lagartos pequeños y ágiles'),
            ('Corytophanidae', 'Basilisco - Lagartos con crestas y capacidad de correr sobre agua'),
            ('Phrynosomatidae', 'Lagartos espinosos - Especies adaptadas a diversos hábitats'),
            ('Gekkonidae', 'Geckos - Lagartos nocturnos con dedos adhesivos'),
            ('Teiidae', 'Lagartos corredores - Especies terrestres y rápidas'),
            ('Scincidae', 'Escíncidos - Lagartos con escamas lisas'),
            ('Xantusiidae', 'Lagartos nocturnos - Especies pequeñas y crípticas'),
        ]

        # Géneros específicos de la región
        generos_saurios = {
            'Iguanidae': [
                ('Iguana', 'Iguanas verdes - Especies grandes y arborícolas'),
                ('Ctenosaura', 'Iguanas espinosas - Especies terrestres con espinas'),
            ],
            'Dactyloidae': [
                ('Anolis', 'Anolis - Lagartos pequeños y coloridos'),
                ('Norops', 'Norops - Subgénero de Anolis'),
            ],
            'Corytophanidae': [
                ('Basiliscus', 'Basilisco - Lagartos con crestas y capacidad de correr sobre agua'),
                ('Corytophanes', 'Lagartos con casco - Especies con crestas prominentes'),
            ],
            'Phrynosomatidae': [
                ('Sceloporus', 'Lagartos espinosos - Especies con escamas espinosas'),
                ('Urosaurus', 'Lagartos de árbol - Especies arborícolas'),
                ('Uta', 'Lagartos de roca - Especies terrestres'),
            ],
            'Gekkonidae': [
                ('Hemidactylus', 'Geckos caseros - Especies introducidas y nativas'),
                ('Thecadactylus', 'Geckos de cola plana - Especies nativas'),
                ('Gonatodes', 'Geckos enanos - Especies pequeñas'),
                ('Sphaerodactylus', 'Geckos esféricos - Especies diminutas'),
            ],
            'Teiidae': [
                ('Aspidoscelis', 'Lagartos corredores - Especies terrestres rápidas'),
                ('Holcosus', 'Lagartos de bosque - Especies de hábitats húmedos'),
                ('Kentropyx', 'Lagartos de pradera - Especies de zonas abiertas'),
            ],
            'Scincidae': [
                ('Lepidophyma', 'Escíncidos nocturnos - Especies con hábitos nocturnos'),
                ('Scincella', 'Escíncidos terrestres - Especies pequeñas'),
            ],
            'Xantusiidae': [
                ('Xantusia', 'Lagartos nocturnos - Especies pequeñas y crípticas'),
            ],
        }

        # Especies específicas de Villahermosa, Tabasco
        especies_saurios = {
            'Iguana': ['iguana', 'rhinolopha'],
            'Ctenosaura': ['pectinata', 'similis', 'acanthura'],
            'Anolis': ['carolinensis', 'sagrei', 'chlorocyanus', 'allisoni', 'porcatus'],
            'Norops': ['humilis', 'limifrons', 'oxylophus', 'tropidolepis'],
            'Basiliscus': ['vittatus', 'plumifrons', 'basiliscus'],
            'Corytophanes': ['cristatus', 'hernandesii', 'percarinatus'],
            'Sceloporus': ['clarkii', 'malachiticus', 'formosus', 'spinosus', 'undulatus'],
            'Urosaurus': ['auriculatus', 'ornatus', 'graciosus'],
            'Uta': ['stansburiana', 'squamata', 'palmeri'],
            'Hemidactylus': ['frenatus', 'turcicus', 'mabouia'],
            'Thecadactylus': ['rapicauda', 'solimoensis'],
            'Gonatodes': ['albogularis', 'humeralis', 'vittatus'],
            'Sphaerodactylus': ['argus', 'elegans', 'glazioui'],
            'Aspidoscelis': ['sexlineata', 'tesselata', 'gularis'],
            'Holcosus': ['undulatus', 'festivus', 'chrysostictus'],
            'Kentropyx': ['calcarata', 'striata', 'borckiana'],
            'Lepidophyma': ['flavimaculatum', 'tuberculatum', 'sylvaticum'],
            'Scincella': ['lateralis', 'cherriei', 'assata'],
            'Xantusia': ['vigilis', 'henshawi', 'riversiana'],
        }

        # Subtipos específicos de saurios
        subtipos_saurios = [
            'Arborícola', 'Terrestre', 'Fosorial', 'Semiacuático', 'No venenoso', 
            'Defensivo', 'Críptico', 'Corredor', 'Escalador', 'Excavador'
        ]

        # Hábitats específicos de Villahermosa, Tabasco
        habitats_saurios = [
            'Selva tropical húmeda', 'Bosque de galería', 'Manglares', 'Sabana tropical',
            'Bosque secundario', 'Zonas urbanas', 'Rocas y acantilados', 'Cuevas y grietas',
            'Áreas de cultivo', 'Pastizales', 'Riberas de ríos', 'Islas fluviales',
            'Áreas pantanosas', 'Bosque de tular', 'Zonas de transición'
        ]

        # Descripciones específicas de la región
        descripciones_saurios = [
            "Saurio endémico de la región de Villahermosa, adaptado a los climas cálidos y húmedos de Tabasco. Presenta coloración verde brillante y excelente capacidad de camuflaje en la vegetación tropical.",
            "Lagarto arborícola común en los bosques de galería del río Grijalva. Se caracteriza por su capacidad de cambiar de color y su comportamiento territorial.",
            "Saurio terrestre que habita en las zonas de sabana y pastizales de la región. Se alimenta principalmente de insectos y pequeños invertebrados.",
            "Lagarto semiacuático que frecuenta los manglares y zonas pantanosas de la costa tabasqueña. Excelente nadador y buceador.",
            "Saurio fosorial que excava madrigueras en suelos arenosos de las zonas costeras. Presenta escamas lisas y cuerpo alargado.",
            "Lagarto de hábitos nocturnos que habita en cuevas y grietas rocosas. Se alimenta de insectos y arañas durante la noche.",
            "Saurio críptico que se camufla perfectamente entre la hojarasca del bosque tropical. Coloración marrón con patrones que imitan hojas secas.",
            "Lagarto corredor que habita en zonas abiertas y soleadas. Muy rápido y ágil, se refugia en grietas cuando se siente amenazado.",
            "Saurio escalador que frecuenta troncos de árboles y paredes rocosas. Presenta dedos prensiles y cola larga para el equilibrio.",
            "Lagarto excavador que construye madrigueras en suelos arcillosos. Se alimenta de larvas de insectos y pequeños invertebrados del suelo.",
            "Saurio de importancia ecológica en el control de poblaciones de insectos en los ecosistemas tropicales de Tabasco.",
            "Lagarto adaptado a las condiciones urbanas de Villahermosa, frecuentemente observado en parques y jardines.",
            "Saurio endémico de los manglares del Golfo de México, con adaptaciones especiales para la vida en ambientes salinos.",
            "Lagarto que habita en las islas fluviales del río Usumacinta, con distribución restringida a este ecosistema único.",
            "Saurio de las zonas de transición entre selva y sabana, con gran capacidad de adaptación a diferentes condiciones ambientales."
        ]

        # Nombres comunes específicos de la región
        nombres_comunes_saurios = [
            'Iguana verde', 'Iguana espinosa', 'Anolis verde', 'Anolis marrón', 'Basilisco común',
            'Lagarto espinoso', 'Gecko casero', 'Gecko de cola plana', 'Lagarto corredor',
            'Escíncido nocturno', 'Lagarto de roca', 'Anolis de árbol', 'Iguana de cola espinosa',
            'Gecko enano', 'Lagarto de bosque', 'Saurio de manglar', 'Lagarto de sabana',
            'Anolis de jardín', 'Gecko de pared', 'Lagarto de río', 'Saurio de cueva',
            'Iguana de galería', 'Anolis de roca', 'Lagarto de pastizal', 'Gecko de hoja',
            'Saurio de transición', 'Lagarto urbano', 'Anolis de isla', 'Iguana de pantano',
            'Gecko de grieta', 'Lagarto de acantilado', 'Saurio de tular', 'Anolis de costa'
        ]

        # Crear familias
        familias_creadas = {}
        for nombre_familia, desc_familia in familias_saurios:
            familia, created = Familia.objects.get_or_create(
                nombre=nombre_familia,
                defaults={'descripcion': desc_familia}
            )
            familias_creadas[nombre_familia] = familia
            if created:
                self.stdout.write(f'Familia creada: {nombre_familia}')

        # Crear géneros
        generos_creados = {}
        for nombre_familia, generos in generos_saurios.items():
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

        # Crear directorio para imágenes si no existe
        ruta_imagenes = os.path.join('static', 'assets', 'saurios_villahermosa')
        if not os.path.exists(ruta_imagenes):
            os.makedirs(ruta_imagenes)
            self.stdout.write(f'Directorio creado: {ruta_imagenes}')

        # Generar imágenes de muestra (usar imágenes específicas de saurios)
        imagenes_base = [
            os.path.join('static', 'assets', 'saurios_villahermosa', 'saurio1.jpg'),
            os.path.join('static', 'assets', 'saurios_villahermosa', 'saurio2.jpg'),
            os.path.join('static', 'assets', 'saurios_villahermosa', 'saurio3.jpg'),
            os.path.join('static', 'assets', 'saurios_villahermosa', 'saurio4.jpg'),
            os.path.join('static', 'assets', 'saurios_villahermosa', 'saurio5.jpg'),
        ]

        # Verificar que existan las imágenes base
        imagenes_disponibles = [img for img in imagenes_base if os.path.exists(img)]
        if not imagenes_disponibles:
            self.stdout.write(self.style.ERROR('No se encontraron imágenes base en static/assets/saurios_villahermosa/'))
            return

        # Crear 350 especies de saurios
        especies_creadas = 0
        for i in range(350):
            # Seleccionar familia y género aleatoriamente
            nombre_familia = random.choice(list(generos_saurios.keys()))
            if nombre_familia in familias_creadas:
                familia = familias_creadas[nombre_familia]
                generos_disponibles = generos_saurios[nombre_familia]
                nombre_genero, desc_genero = random.choice(generos_disponibles)
                
                if nombre_genero in generos_creados:
                    genero = generos_creados[nombre_genero]
                    
                    # Seleccionar especie
                    if nombre_genero in especies_saurios:
                        nombre_especie = random.choice(especies_saurios[nombre_genero])
                    else:
                        nombre_especie = f"sp{i+1}"
                    
                    # Evitar duplicados
                    if Especie.objects.filter(genero=genero, nombre_especie=nombre_especie).exists():
                        nombre_especie = f"{nombre_especie}_{i+1}"
                    
                    # Crear la especie
                    especie = Especie.objects.create(
                        genero=genero,
                        nombre_especie=nombre_especie,
                        nombre_comun=random.choice(nombres_comunes_saurios),
                        tipo_animal='Saurio',
                        subtipo=random.choice(subtipos_saurios),
                        habitat=random.choice(habitats_saurios),
                        descripcion=random.choice(descripciones_saurios),
                        peligro_extincion=random.choice([True, False, False, False, False])
                    )
                    
                    # Asignar imagen
                    imagen_path = random.choice(imagenes_disponibles)
                    try:
                        with open(imagen_path, 'rb') as img_file:
                            especie.imagen.save(
                                f'saurio_villahermosa_{especie.id}.jpg',
                                File(img_file),
                                save=True
                            )
                        especies_creadas += 1
                        
                        if especies_creadas % 50 == 0:
                            self.stdout.write(f'Progreso: {especies_creadas} especies creadas...')
                            
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Error al asignar imagen a especie {especie.id}: {e}'))
                        especies_creadas += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'¡Completado! Se crearon {especies_creadas} especies de saurios de Villahermosa, Tabasco, México.'
            )
        ) 