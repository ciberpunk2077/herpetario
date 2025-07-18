import os
import django
import random
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from PIL import Image
import io

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herpetario.settings')
django.setup()

from apps.catalogo.models import Familia, Genero, Especie

# Datos de serpientes específicas de Tabasco con variaciones
serpientes_tabasco = [
    # Viperidae (Víboras)
    {
        'familia': 'Viperidae',
        'genero': 'Bothriechis',
        'especie': 'schlegelii',
        'nombre_comun': 'Víbora de pestañas',
        'subtipo': 'Venenosa',
        'habitat': 'Selva húmeda, árboles y arbustos',
        'descripcion': 'Serpiente venenosa arbórea con escamas modificadas sobre los ojos que parecen pestañas. Habita en la selva húmeda de Tabasco, especialmente en zonas con vegetación densa.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Bothriechis',
        'especie': 'aurifer',
        'nombre_comun': 'Víbora de árbol amarilla',
        'subtipo': 'Venenosa',
        'habitat': 'Bosque tropical, árboles',
        'descripcion': 'Víbora venenosa de coloración amarilla a verde, muy arbórea. Se encuentra en los bosques tropicales de Tabasco, especialmente en zonas montañosas.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Crotalus',
        'especie': 'durissus',
        'nombre_comun': 'Cascabel tropical',
        'subtipo': 'Venenosa',
        'habitat': 'Sabanas, pastizales, zonas semiáridas',
        'descripcion': 'Serpiente de cascabel que habita en las sabanas y pastizales de Tabasco. Su veneno es neurotóxico y puede ser mortal.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Agkistrodon',
        'especie': 'bilineatus',
        'nombre_comun': 'Cantil',
        'subtipo': 'Venenosa',
        'habitat': 'Ríos, lagunas, zonas húmedas',
        'descripcion': 'Serpiente venenosa semiacuática que habita en ríos y lagunas de Tabasco. Es excelente nadadora y cazadora.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Porthidium',
        'especie': 'nasutum',
        'nombre_comun': 'Víbora nariz de cerdo',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Víbora terrestre con hocico levantado característico. Habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Bothriechis',
        'especie': 'lateralis',
        'nombre_comun': 'Víbora de árbol verde',
        'subtipo': 'Venenosa',
        'habitat': 'Árboles, selva tropical',
        'descripcion': 'Víbora arbórea de color verde brillante. Habita en los árboles de la selva tropical de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Crotalus',
        'especie': 'simus',
        'nombre_comun': 'Cascabel centroamericano',
        'subtipo': 'Venenosa',
        'habitat': 'Bosque seco, zonas rocosas',
        'descripcion': 'Serpiente de cascabel que habita en zonas rocosas y bosques secos de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Bothriechis',
        'especie': 'supraciliaris',
        'nombre_comun': 'Víbora de cejas',
        'subtipo': 'Venenosa',
        'habitat': 'Árboles, selva tropical',
        'descripcion': 'Víbora arbórea con escamas modificadas sobre las cejas. Habita en la selva tropical de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Porthidium',
        'especie': 'ophryomegas',
        'nombre_comun': 'Víbora nariz de cerdo de cejas',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Víbora terrestre con hocico y cejas características. Habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Viperidae',
        'genero': 'Agkistrodon',
        'especie': 'taylori',
        'nombre_comun': 'Cantil de Taylor',
        'subtipo': 'Venenosa',
        'habitat': 'Ríos, lagunas, zonas húmedas',
        'descripcion': 'Serpiente venenosa semiacuática que habita en ríos y lagunas de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    
    # Colubridae (Culebras)
    {
        'familia': 'Colubridae',
        'genero': 'Drymobius',
        'especie': 'margaritiferus',
        'nombre_comun': 'Culebra verde esmeralda',
        'subtipo': 'No venenosa',
        'habitat': 'Selva, jardines, vegetación densa',
        'descripcion': 'Culebra no venenosa de color verde esmeralda brillante. Muy común en los jardines y vegetación de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Leptophis',
        'especie': 'ahactulla',
        'nombre_comun': 'Culebra liana',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, lianas, vegetación arbórea',
        'descripcion': 'Culebra delgada y larga que se mueve con agilidad entre las lianas y ramas de los árboles en la selva de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Spilotes',
        'especie': 'pullatus',
        'nombre_comun': 'Culebra tigre',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, selva, zonas rurales',
        'descripcion': 'Culebra grande y robusta con patrón de bandas negras y amarillas. Excelente trepadora que habita en la selva de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Mastigodryas',
        'especie': 'melanolomus',
        'nombre_comun': 'Culebra café',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, zonas rurales',
        'descripcion': 'Culebra terrestre de color café que se alimenta principalmente de roedores. Común en zonas rurales de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Oxybelis',
        'especie': 'aeneus',
        'nombre_comun': 'Culebra nariz de lanza',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, vegetación',
        'descripcion': 'Culebra muy delgada con hocico puntiagudo. Se camufla perfectamente entre las ramas de los árboles en Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Tantilla',
        'especie': 'melanocephala',
        'nombre_comun': 'Culebra cabeza negra',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña con cabeza negra distintiva. Se alimenta de insectos y arañas en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Lampropeltis',
        'especie': 'triangulum',
        'nombre_comun': 'Culebra rey',
        'subtipo': 'No venenosa',
        'habitat': 'Bosque, pastizales, zonas rurales',
        'descripcion': 'Culebra con patrón de bandas rojas, negras y blancas. Se alimenta de otras serpientes, incluyendo venenosas.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Coluber',
        'especie': 'constrictor',
        'nombre_comun': 'Culebra corredora',
        'subtipo': 'No venenosa',
        'habitat': 'Pastizales, campos abiertos',
        'descripcion': 'Culebra rápida y ágil que habita en pastizales y campos abiertos de Tabasco. Excelente cazadora.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Drymobius',
        'especie': 'chloroticus',
        'nombre_comun': 'Culebra verde clara',
        'subtipo': 'No venenosa',
        'habitat': 'Vegetación, jardines, zonas urbanas',
        'descripcion': 'Culebra de color verde claro que se adapta bien a zonas urbanas de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Leptophis',
        'especie': 'depressirostris',
        'nombre_comun': 'Culebra liana de hocico plano',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, lianas, vegetación densa',
        'descripcion': 'Culebra arbórea con hocico característicamente aplanado. Habita en la vegetación densa de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Mastigodryas',
        'especie': 'boddaerti',
        'nombre_comun': 'Culebra café de Boddaert',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Culebra terrestre de color café oscuro. Habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Tantilla',
        'especie': 'rubra',
        'nombre_comun': 'Culebra cabeza negra rojiza',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña con cabeza negra y cuerpo rojizo. Se alimenta de insectos en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Drymobius',
        'especie': 'multicinctus',
        'nombre_comun': 'Culebra verde multibanda',
        'subtipo': 'No venenosa',
        'habitat': 'Vegetación, jardines, zonas urbanas',
        'descripcion': 'Culebra verde con múltiples bandas. Se adapta bien a zonas urbanas de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Leptophis',
        'especie': 'mexicanus',
        'nombre_comun': 'Culebra liana mexicana',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, lianas, vegetación densa',
        'descripcion': 'Culebra arbórea mexicana que habita en la vegetación densa de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Mastigodryas',
        'especie': 'cliftoni',
        'nombre_comun': 'Culebra café de Clifton',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Culebra terrestre que habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Tantilla',
        'especie': 'calamarina',
        'nombre_comun': 'Culebra cabeza negra de calamar',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña con cabeza negra. Se alimenta de insectos en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Oxybelis',
        'especie': 'brevirostris',
        'nombre_comun': 'Culebra nariz de lanza corta',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, vegetación',
        'descripcion': 'Culebra delgada con hocico corto. Se camufla entre las ramas de los árboles en Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Colubridae',
        'genero': 'Lampropeltis',
        'especie': 'polyzona',
        'nombre_comun': 'Culebra rey de múltiples zonas',
        'subtipo': 'No venenosa',
        'habitat': 'Bosque, pastizales, zonas rurales',
        'descripcion': 'Culebra rey con múltiples zonas de color. Se alimenta de otras serpientes en Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    
    # Boidae (Boa)
    {
        'familia': 'Boidae',
        'genero': 'Boa',
        'especie': 'constrictor',
        'nombre_comun': 'Boa constrictor',
        'subtipo': 'Constrictora',
        'habitat': 'Selva, bosque, zonas rurales',
        'descripcion': 'Serpiente grande y poderosa que mata por constricción. Habita en la selva de Tabasco y puede alcanzar hasta 4 metros.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Boidae',
        'genero': 'Corallus',
        'especie': 'hortulanus',
        'nombre_comun': 'Boa arborícola',
        'subtipo': 'Constrictora',
        'habitat': 'Árboles, selva tropical',
        'descripcion': 'Boa arbórea que habita en los árboles de la selva tropical de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Boidae',
        'genero': 'Corallus',
        'especie': 'annulatus',
        'nombre_comun': 'Boa arborícola anillada',
        'subtipo': 'Constrictora',
        'habitat': 'Árboles, selva tropical',
        'descripcion': 'Boa arbórea con patrón anillado. Habita en los árboles de la selva tropical de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    
    # Elapidae (Coralillos)
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'fulvius',
        'nombre_comun': 'Coralillo del este',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, zonas boscosas',
        'descripcion': 'Serpiente venenosa con patrón de bandas rojas, amarillas y negras. Su veneno es neurotóxico y muy peligroso.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'diastema',
        'nombre_comun': 'Coralillo variable',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Coralillo con patrón variable de bandas. Habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'nigrocinctus',
        'nombre_comun': 'Coralillo centroamericano',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque tropical',
        'descripcion': 'Coralillo con patrón distintivo de bandas. Habita en los bosques tropicales de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'alleni',
        'nombre_comun': 'Coralillo de Allen',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Coralillo con patrón específico de bandas. Habita en los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'elegans',
        'nombre_comun': 'Coralillo elegante',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Coralillo con patrón elegante de bandas. Habita en los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Elapidae',
        'genero': 'Micrurus',
        'especie': 'limbatus',
        'nombre_comun': 'Coralillo de bordes',
        'subtipo': 'Venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Coralillo con bordes distintivos en sus bandas. Habita en los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    
    # Dipsadidae (Culebras de tierra)
    {
        'familia': 'Dipsadidae',
        'genero': 'Imantodes',
        'especie': 'cenchoa',
        'nombre_comun': 'Culebra látigo',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, vegetación',
        'descripcion': 'Culebra extremadamente delgada que se mueve como un látigo entre las ramas. Muy común en la vegetación de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Leptodeira',
        'especie': 'annulata',
        'nombre_comun': 'Culebra de ojos de gato',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, zonas húmedas',
        'descripcion': 'Culebra con pupilas verticales como las de un gato. Se alimenta principalmente de ranas y lagartijas.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Ninia',
        'especie': 'sebae',
        'nombre_comun': 'Culebra enana',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña que raramente supera los 30 cm. Se alimenta de insectos y pequeños invertebrados.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Geophis',
        'especie': 'semidoliatus',
        'nombre_comun': 'Culebra de tierra',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Culebra terrestre que habita en el suelo de los bosques de Tabasco. Se alimenta de lombrices y pequeños invertebrados.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Coniophanes',
        'especie': 'imperialis',
        'nombre_comun': 'Culebra rayada',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra con patrón de rayas longitudinales. Habita en jardines y zonas rurales de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Imantodes',
        'especie': 'inornatus',
        'nombre_comun': 'Culebra látigo sin adornos',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, vegetación',
        'descripcion': 'Culebra látigo sin patrones distintivos. Habita en la vegetación de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Leptodeira',
        'especie': 'septentrionalis',
        'nombre_comun': 'Culebra de ojos de gato septentrional',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, zonas húmedas',
        'descripcion': 'Culebra con pupilas verticales que habita en zonas húmedas de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Ninia',
        'especie': 'atrata',
        'nombre_comun': 'Culebra enana negra',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña de coloración oscura. Se alimenta de insectos en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Geophis',
        'especie': 'dubius',
        'nombre_comun': 'Culebra de tierra dudosa',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Culebra terrestre que habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Coniophanes',
        'especie': 'piceivittis',
        'nombre_comun': 'Culebra rayada de vientre rojo',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra con rayas y vientre rojizo. Habita en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Imantodes',
        'especie': 'gemmistratus',
        'nombre_comun': 'Culebra látigo de gemas',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, vegetación',
        'descripcion': 'Culebra látigo con patrón de gemas. Habita en la vegetación de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Leptodeira',
        'especie': 'bakeri',
        'nombre_comun': 'Culebra de ojos de gato de Baker',
        'subtipo': 'No venenosa',
        'habitat': 'Árboles, arbustos, zonas húmedas',
        'descripcion': 'Culebra con pupilas verticales que habita en zonas húmedas de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Ninia',
        'especie': 'diademata',
        'nombre_comun': 'Culebra enana diademada',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra pequeña con patrón de diadema. Se alimenta de insectos en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Geophis',
        'especie': 'ruthveni',
        'nombre_comun': 'Culebra de tierra de Ruthven',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, bosque',
        'descripcion': 'Culebra terrestre que habita en el suelo de los bosques de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Dipsadidae',
        'genero': 'Coniophanes',
        'especie': 'quinquivittatus',
        'nombre_comun': 'Culebra rayada de cinco bandas',
        'subtipo': 'No venenosa',
        'habitat': 'Suelo, hojarasca, jardines',
        'descripcion': 'Culebra con cinco bandas longitudinales. Habita en jardines de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    
    # Natricidae (Culebras de agua)
    {
        'familia': 'Natricidae',
        'genero': 'Nerodia',
        'especie': 'rhombifer',
        'nombre_comun': 'Culebra de agua diamante',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, lagunas, pantanos',
        'descripcion': 'Culebra semiacuática que habita en ríos y lagunas de Tabasco. Excelente nadadora y pescadora.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Natricidae',
        'genero': 'Thamnophis',
        'especie': 'proximus',
        'nombre_comun': 'Culebra listonada',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, arroyos, zonas húmedas',
        'descripcion': 'Culebra con patrón de listones longitudinales. Habita en ríos y arroyos de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Natricidae',
        'genero': 'Nerodia',
        'especie': 'fasciata',
        'nombre_comun': 'Culebra de agua bandeada',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, lagunas, pantanos',
        'descripcion': 'Culebra de agua con bandas transversales. Habita en cuerpos de agua de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Natricidae',
        'genero': 'Thamnophis',
        'especie': 'marcianus',
        'nombre_comun': 'Culebra listonada de Marcy',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, arroyos, zonas húmedas',
        'descripcion': 'Culebra listonada que habita en ríos y arroyos de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Natricidae',
        'genero': 'Nerodia',
        'especie': 'erythrogaster',
        'nombre_comun': 'Culebra de agua de vientre rojo',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, lagunas, pantanos',
        'descripcion': 'Culebra de agua con vientre rojizo. Habita en cuerpos de agua de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    },
    {
        'familia': 'Natricidae',
        'genero': 'Thamnophis',
        'especie': 'sirtalis',
        'nombre_comun': 'Culebra listonada común',
        'subtipo': 'No venenosa',
        'habitat': 'Ríos, arroyos, zonas húmedas',
        'descripcion': 'Culebra listonada común que habita en ríos y arroyos de Tabasco.',
        'imagen_url': 'https://images.unsplash.com/photo-1559251606-c623743a6d76?w=400&h=300&fit=crop'
    }
]

def descargar_imagen(url, nombre_archivo):
    """Descarga una imagen desde URL y la guarda localmente"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Crear imagen con PIL para optimizar
        img = Image.open(io.BytesIO(response.content))
        img = img.convert('RGB')
        
        # Redimensionar si es muy grande
        if img.width > 800 or img.height > 600:
            img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Guardar imagen optimizada
        ruta_archivo = f'static/assets/images/serpientes_tabasco/{nombre_archivo}.jpg'
        img.save(ruta_archivo, 'JPEG', quality=85, optimize=True)
        
        return ruta_archivo
    except Exception as e:
        print(f"Error descargando imagen para {nombre_archivo}: {e}")
        return None

def crear_familias_y_generos():
    """Crear las familias y géneros necesarios"""
    familias_creadas = {}
    generos_creados = {}
    
    for serpiente in serpientes_tabasco:
        # Crear familia si no existe
        if serpiente['familia'] not in familias_creadas:
            familia, created = Familia.objects.get_or_create(
                nombre=serpiente['familia'],
                defaults={'descripcion': f'Familia de serpientes {serpiente["familia"]}'}
            )
            familias_creadas[serpiente['familia']] = familia
            if created:
                print(f"Familia creada: {serpiente['familia']}")
        
        # Crear género si no existe
        genero_key = f"{serpiente['genero']}_{serpiente['familia']}"
        if genero_key not in generos_creados:
            genero, created = Genero.objects.get_or_create(
                nombre=serpiente['genero'],
                familia=familias_creadas[serpiente['familia']],
                defaults={'descripcion': f'Género {serpiente["genero"]} de la familia {serpiente["familia"]}'}
            )
            generos_creados[genero_key] = genero
            if created:
                print(f"Género creado: {serpiente['genero']}")

def crear_serpientes():
    """Crear las serpientes de Tabasco"""
    print("Iniciando creación de serpientes de Tabasco...")
    
    # Crear familias y géneros primero
    crear_familias_y_generos()
    
    # Obtener referencias a familias y géneros
    familias = {f.nombre: f for f in Familia.objects.all()}
    generos = {f"{g.nombre}_{g.familia.nombre}": g for g in Genero.objects.all()}
    
    serpientes_creadas = 0
    
    for serpiente in serpientes_tabasco:
        try:
            genero = generos[f"{serpiente['genero']}_{serpiente['familia']}"]
            
            # Verificar si ya existe
            if Especie.objects.filter(genero=genero, nombre_especie=serpiente['especie']).exists():
                print(f"Serpiente ya existe: {serpiente['genero']} {serpiente['especie']}")
                continue
            
            # Descargar imagen
            nombre_imagen = f"{serpiente['genero'].lower()}_{serpiente['especie'].lower()}"
            ruta_imagen = descargar_imagen(serpiente['imagen_url'], nombre_imagen)
            
            # Crear la especie
            nueva_serpiente = Especie.objects.create(
                genero=genero,
                nombre_especie=serpiente['especie'],
                nombre_comun=serpiente['nombre_comun'],
                tipo_animal='Serpiente',
                subtipo=serpiente['subtipo'],
                habitat=serpiente['habitat'],
                descripcion=serpiente['descripcion'],
                peligro_extincion=random.choice([True, False])  # Algunas en peligro
            )
            
            # Asignar imagen si se descargó correctamente
            if ruta_imagen and os.path.exists(ruta_imagen):
                with open(ruta_imagen, 'rb') as img_file:
                    nueva_serpiente.imagen.save(
                        f"{nombre_imagen}.jpg",
                        File(img_file),
                        save=True
                    )
            
            serpientes_creadas += 1
            print(f"Serpiente creada {serpientes_creadas}/50: {nueva_serpiente.nombre_cientifico}")
            
        except Exception as e:
            print(f"Error creando serpiente {serpiente['genero']} {serpiente['especie']}: {e}")
    
    print(f"\n¡Proceso completado! Se crearon {serpientes_creadas} serpientes de Tabasco.")
    print("Las serpientes incluyen especies venenosas y no venenosas, arbóreas y terrestres.")
    print("Todas las especies son nativas o comunes en el estado de Tabasco.")
    print("\nEspecies incluidas:")
    print("- Víboras venenosas (Bothriechis, Crotalus, Agkistrodon, Porthidium)")
    print("- Culebras no venenosas (Drymobius, Leptophis, Spilotes, Mastigodryas)")
    print("- Boas constrictoras (Boa, Corallus)")
    print("- Coralillos venenosos (Micrurus)")
    print("- Culebras especializadas (Imantodes, Leptodeira, Ninia, Geophis, Coniophanes)")
    print("- Culebras de agua (Nerodia, Thamnophis)")

if __name__ == '__main__':
    crear_serpientes() 