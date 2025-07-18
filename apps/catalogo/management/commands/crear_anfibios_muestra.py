import os
import requests
import tempfile
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from apps.catalogo.models import Familia, Genero, Especie
import random

class Command(BaseCommand):
    help = 'Crea 500 registros de anfibios con datos realistas e imágenes locales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Número de anfibios a crear (default: 500)'
        )

    def handle(self, *args, **options):
        count = options['count']
        # --- NUEVO: Eliminar registros previos de Anfibio ---
        self.stdout.write('Eliminando registros previos de Anfibio...')
        from apps.catalogo.models import Especie, Genero, Familia
        Especie.objects.filter(tipo_animal='Anfibio').delete()
        Genero.objects.filter(familia__nombre__in=[
            'Bufonidae', 'Hylidae', 'Ranidae', 'Dendrobatidae', 'Plethodontidae',
            'Salamandridae', 'Ambystomatidae', 'Cryptobranchidae', 'Proteidae', 'Sirenidae'
        ]).delete()
        Familia.objects.filter(nombre__in=[
            'Bufonidae', 'Hylidae', 'Ranidae', 'Dendrobatidae', 'Plethodontidae',
            'Salamandridae', 'Ambystomatidae', 'Cryptobranchidae', 'Proteidae', 'Sirenidae'
        ]).delete()
        self.stdout.write('Registros previos eliminados.')
        
        # Datos realistas de anfibios
        familias_anfibios = [
            ('Bufonidae', 'Sapos verdaderos'),
            ('Hylidae', 'Ranas arborícolas'),
            ('Ranidae', 'Ranas verdaderas'),
            ('Dendrobatidae', 'Ranas venenosas'),
            ('Plethodontidae', 'Salamandras sin pulmones'),
            ('Salamandridae', 'Salamandras verdaderas'),
            ('Ambystomatidae', 'Salamandras topo'),
            ('Cryptobranchidae', 'Salamandras gigantes'),
            ('Proteidae', 'Proteos'),
            ('Sirenidae', 'Sirenas'),
        ]

        generos_anfibios = {
            'Bufonidae': [
                ('Bufo', 'Sapos comunes'),
                ('Anaxyrus', 'Sapos americanos'),
                ('Rhinella', 'Sapos sudamericanos'),
                ('Duttaphrynus', 'Sapos asiáticos'),
                ('Epidalea', 'Sapos europeos'),
            ],
            'Hylidae': [
                ('Hyla', 'Ranas arborícolas verdaderas'),
                ('Acris', 'Ranas grillo'),
                ('Pseudacris', 'Ranas coro'),
                ('Litoria', 'Ranas australianas'),
                ('Agalychnis', 'Ranas de ojos rojos'),
            ],
            'Ranidae': [
                ('Rana', 'Ranas verdaderas'),
                ('Lithobates', 'Ranas americanas'),
                ('Pelophylax', 'Ranas verdes'),
                ('Amolops', 'Ranas de cascada'),
                ('Odorrana', 'Ranas olorosas'),
            ],
            'Dendrobatidae': [
                ('Dendrobates', 'Ranas venenosas'),
                ('Phyllobates', 'Ranas doradas'),
                ('Oophaga', 'Ranas flecha'),
                ('Ameerega', 'Ranas venenosas sudamericanas'),
                ('Epipedobates', 'Ranas venenosas de tres rayas'),
            ],
            'Plethodontidae': [
                ('Plethodon', 'Salamandras sin pulmones'),
                ('Desmognathus', 'Salamandras de arroyo'),
                ('Eurycea', 'Salamandras de manantial'),
                ('Batrachoseps', 'Salamandras delgadas'),
                ('Aneides', 'Salamandras trepadoras'),
            ],
            'Salamandridae': [
                ('Salamandra', 'Salamandras de fuego'),
                ('Triturus', 'Tritones'),
                ('Notophthalmus', 'Tritones americanos'),
                ('Taricha', 'Salamandras del Pacífico'),
                ('Cynops', 'Tritones asiáticos'),
            ],
            'Ambystomatidae': [
                ('Ambystoma', 'Salamandras topo'),
                ('Dicamptodon', 'Salamandras gigantes del Pacífico'),
                ('Rhyacotriton', 'Salamandras de cascada'),
            ],
            'Cryptobranchidae': [
                ('Cryptobranchus', 'Salamandras gigantes americanas'),
                ('Andrias', 'Salamandras gigantes asiáticas'),
            ],
            'Proteidae': [
                ('Proteus', 'Proteos'),
                ('Necturus', 'Mudpuppies'),
            ],
            'Sirenidae': [
                ('Siren', 'Sirenas'),
                ('Pseudobranchus', 'Sirenas enanas'),
            ],
        }

        especies_anfibios = {
            'Bufo': ['bufo', 'calamita', 'viridis', 'marinus', 'regularis'],
            'Anaxyrus': ['americanus', 'fowleri', 'terrestris', 'woodhousii', 'cognatus'],
            'Rhinella': ['marina', 'jimi', 'schneideri', 'granulosa', 'arenarum'],
            'Duttaphrynus': ['melanostictus', 'stomaticus', 'microscaphus', 'scaber', 'brevipollicatus'],
            'Epidalea': ['calamita', 'viridis', 'bufo'],
            'Hyla': ['cinerea', 'versicolor', 'chrysoscelis', 'gratiosa', 'femoralis'],
            'Acris': ['crepitans', 'gryllus', 'blanchardi'],
            'Pseudacris': ['crucifer', 'triseriata', 'maculata', 'clarkii', 'ornata'],
            'Litoria': ['caerulea', 'chloris', 'fallax', 'infrafrenata', 'tyleri'],
            'Agalychnis': ['callidryas', 'saltator', 'spurrelli', 'annae', 'dacnicolor'],
            'Rana': ['temporaria', 'ridibunda', 'esculenta', 'lessonae', 'dalmatina'],
            'Lithobates': ['catesbeianus', 'clamitans', 'pipiens', 'sphenocephalus', 'palustris'],
            'Pelophylax': ['ridibundus', 'esculentus', 'lessonae', 'perezi', 'nigromaculatus'],
            'Amolops': ['ricketti', 'torrentis', 'formosus', 'mantzorum', 'loloensis'],
            'Odorrana': ['margaretae', 'schmackeri', 'tormota', 'versabilis', 'andersonii'],
            'Dendrobates': ['tinctorius', 'leucomelas', 'auratus', 'truncatus', 'fantastica'],
            'Phyllobates': ['terribilis', 'bicolor', 'aurotaenia', 'lugubris', 'vitattus'],
            'Oophaga': ['pumilio', 'histrionica', 'lehmanni', 'vicentei', 'granulifera'],
            'Ameerega': ['trivittata', 'hahneli', 'pulchripecta', 'flavopicta', 'braccata'],
            'Epipedobates': ['tricolor', 'anthonyi', 'boulengeri', 'espinosai', 'darwinwallacei'],
            'Plethodon': ['cinereus', 'glutinosus', 'serratus', 'yonahlossee', 'welleri'],
            'Desmognathus': ['fuscus', 'ochrophaeus', 'monticola', 'quadramaculatus', 'wrighti'],
            'Eurycea': ['bislineata', 'longicauda', 'lucifuga', 'guttolineata', 'quadridigitata'],
            'Batrachoseps': ['attenuatus', 'nigriventris', 'wrighti', 'relictus', 'major'],
            'Aneides': ['aeneus', 'ferreus', 'flavipunctatus', 'hardii', 'lugubris'],
            'Salamandra': ['salamandra', 'algira', 'infraimmaculata', 'corsica', 'atra'],
            'Triturus': ['cristatus', 'marmoratus', 'alpestris', 'vulgaris', 'helveticus'],
            'Notophthalmus': ['viridescens', 'perstriatus', 'meridionalis'],
            'Taricha': ['torosa', 'granulosa', 'rivularis', 'sierrae'],
            'Cynops': ['pyrrhogaster', 'ensicauda', 'orientalis', 'cyanurus', 'wolterstorffi'],
            'Ambystoma': ['mexicanum', 'tigrinum', 'maculatum', 'opacum', 'jeffersonianum'],
            'Dicamptodon': ['ensatus', 'aterrimus', 'tenebrosus', 'copei'],
            'Rhyacotriton': ['olympicus', 'kezeri', 'cascadae', 'variegatus'],
            'Cryptobranchus': ['alleganiensis', 'bishopi'],
            'Andrias': ['japonicus', 'davidianus'],
            'Proteus': ['anguinus'],
            'Necturus': ['maculosus', 'punctatus', 'lewisi', 'alabamensis'],
            'Siren': ['lacertina', 'intermedia', 'reticulata'],
            'Pseudobranchus': ['striatus', 'axanthus'],
        }

        subtipos_anfibios = [
            'Acuático', 'Terrestre', 'Arborícola', 'Fosorial', 'Semiacuático',
            'Veneno', 'Tóxico', 'No venenoso', 'Defensivo', 'Criptico'
        ]

        habitats_anfibios = [
            'Bosque tropical húmedo', 'Bosque templado', 'Selva amazónica',
            'Pantanos y humedales', 'Ríos y arroyos', 'Lagos y estanques',
            'Montañas tropicales', 'Bosque de niebla', 'Sabanas húmedas',
            'Cuevas y cavernas', 'Ríos de montaña', 'Charcas temporales',
            'Bosque seco tropical', 'Manglares', 'Bosque nuboso',
            'Ríos de corriente rápida', 'Estanques artificiales', 'Bosque lluvioso',
            'Humedales costeros', 'Bosque de galería'
        ]

        descripciones_anfibios = [
            "Especie de anfibio caracterizada por su adaptabilidad a diversos hábitats. Presenta una coloración variable que le permite camuflarse eficazmente en su entorno natural.",
            "Anfibio de hábitos principalmente nocturnos, que emerge durante la noche para alimentarse de pequeños invertebrados. Su piel es permeable y sensible a los cambios ambientales.",
            "Especie endémica con distribución limitada a regiones específicas. Su supervivencia depende de la conservación de su hábitat natural y la calidad del agua.",
            "Anfibio con capacidad de regeneración notable, capaz de regenerar extremidades y otros tejidos. Es un indicador importante de la salud del ecosistema.",
            "Especie con comportamiento reproductivo complejo, que incluye rituales de apareamiento elaborados y cuidado parental en algunas poblaciones.",
            "Anfibio adaptado a condiciones extremas, capaz de sobrevivir en ambientes con variaciones significativas de temperatura y humedad.",
            "Especie con vocalizaciones distintivas utilizadas para comunicación territorial y atracción de parejas durante la temporada reproductiva.",
            "Anfibio con estrategias de defensa sofisticadas, incluyendo secreciones cutáneas tóxicas y comportamiento de escape altamente desarrollado.",
            "Especie con ciclo de vida complejo que incluye metamorfosis completa, desde huevos acuáticos hasta adultos terrestres o semiacuáticos.",
            "Anfibio con requerimientos específicos de hábitat, que incluye la necesidad de cuerpos de agua limpios para la reproducción y desarrollo larval.",
            "Especie con distribución geográfica amplia pero fragmentada, enfrentando amenazas por pérdida de hábitat y contaminación ambiental.",
            "Anfibio con adaptaciones especializadas para su modo de vida, incluyendo modificaciones en la estructura de la piel y sistema respiratorio.",
            "Especie con comportamiento social complejo, que incluye agregaciones reproductivas y sistemas de comunicación química sofisticados.",
            "Anfibio con capacidad de hibernación y estivación, adaptado a climas con estaciones marcadas y períodos de escasez de recursos.",
            "Especie con importancia ecológica significativa, actuando como depredador de invertebrados y presa para otros animales en la cadena trófica.",
            "Anfibio con requerimientos microclimáticos específicos, que incluye rangos estrechos de temperatura y humedad para su supervivencia.",
            "Especie con estrategias reproductivas variadas, desde reproducción directa hasta desarrollo larval acuático prolongado.",
            "Anfibio con capacidad de dispersión limitada, lo que lo hace vulnerable a la fragmentación del hábitat y cambios ambientales.",
            "Especie con adaptaciones para la vida en ambientes extremos, incluyendo tolerancia a altas temperaturas y baja disponibilidad de agua.",
            "Anfibio con importancia cultural y científica, utilizado en investigaciones biomédicas y conservación de ecosistemas."
        ]

        nombres_comunes_anfibios = [
            'Rana verde común', 'Sapo americano', 'Salamandra de fuego', 'Tritón crestado',
            'Rana arborícola', 'Sapo europeo', 'Salamandra sin pulmones', 'Rana venenosa',
            'Tritón alpino', 'Sapo gigante', 'Rana de ojos rojos', 'Salamandra gigante',
            'Rana de cascada', 'Sapo asiático', 'Tritón americano', 'Rana coro',
            'Salamandra topo', 'Rana dorada', 'Sapo sudamericano', 'Tritón europeo',
            'Rana de manantial', 'Salamandra del Pacífico', 'Rana grillo', 'Sapo africano',
            'Tritón asiático', 'Rana de charca', 'Salamandra de arroyo', 'Rana australiana',
            'Sapo australiano', 'Tritón crestado', 'Rana de bosque', 'Salamandra de montaña',
            'Rana de río', 'Sapo de caña', 'Tritón jaspeado', 'Rana de pantano',
            'Salamandra de cueva', 'Rana de estanque', 'Sapo de jardín', 'Tritón palmeado',
            'Rana de humedal', 'Salamandra de galería', 'Rana de sierra', 'Sapo de desierto',
            'Tritón de montaña', 'Rana de valle', 'Salamandra de bosque', 'Rana de pradera',
            'Sapo de montaña', 'Tritón de lago', 'Rana de colina', 'Salamandra de río'
        ]

        # Crear familias si no existen
        familias_creadas = {}
        for nombre_familia, desc_familia in familias_anfibios:
            familia, created = Familia.objects.get_or_create(
                nombre=nombre_familia,
                defaults={'descripcion': desc_familia}
            )
            familias_creadas[nombre_familia] = familia
            if created:
                self.stdout.write(f'Familia creada: {nombre_familia}')

        # Crear géneros si no existen
        generos_creados = {}
        for nombre_familia, generos in generos_anfibios.items():
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

        # --- NUEVO: Obtener lista de imágenes locales ---
        ruta_imagenes = os.path.join('static', 'assets', 'anfibios_muestra')
        imagenes_locales = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if f.lower().endswith(('.jpg','.jpeg','.png'))]
        if not imagenes_locales:
            self.stdout.write(self.style.ERROR('No se encontraron imágenes en static/assets/anfibios_muestra/'))
            return

        # Crear especies de anfibios
        especies_creadas = 0
        for i in range(count):
            # Seleccionar familia y género aleatoriamente
            nombre_familia = random.choice(list(generos_anfibios.keys()))
            familia = familias_creadas[nombre_familia]
            nombre_genero = random.choice(generos_anfibios[nombre_familia])[0]
            genero = generos_creados[nombre_genero]
            
            # Seleccionar especie aleatoriamente
            if nombre_genero in especies_anfibios:
                nombre_especie = random.choice(especies_anfibios[nombre_genero])
            else:
                nombre_especie = f"sp{i+1}"
            
            # Verificar si la especie ya existe
            if Especie.objects.filter(genero=genero, nombre_especie=nombre_especie).exists():
                nombre_especie = f"{nombre_especie}_{i+1}"
            
            # Crear la especie
            especie = Especie.objects.create(
                genero=genero,
                nombre_especie=nombre_especie,
                nombre_comun=random.choice(nombres_comunes_anfibios),
                tipo_animal='Anfibio',
                subtipo=random.choice(subtipos_anfibios),
                habitat=random.choice(habitats_anfibios),
                descripcion=random.choice(descripciones_anfibios),
                peligro_extincion=random.choice([True, False, False, False])  # 25% en peligro
            )
            
            # Asignar imagen local aleatoria
            imagen_path = random.choice(imagenes_locales)
            with open(imagen_path, 'rb') as img_file:
                especie.imagen.save(
                    f'anfibio_{especie.id}.jpg',
                    File(img_file),
                    save=True
                )
            
            especies_creadas += 1
            if especies_creadas % 50 == 0:
                self.stdout.write(f'Creadas {especies_creadas} especies de anfibios...')

        self.stdout.write(
            self.style.SUCCESS(
                f'¡Completado! Se crearon {especies_creadas} especies de anfibios con imágenes locales.'
            )
        ) 