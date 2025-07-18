from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.catalogo.views import *
from apps.catalogo.view.familia import *
from apps.catalogo.view.serpiente import *
from apps.catalogo.view.anfibio import *
from apps.catalogo.view.saurio import *
from apps.catalogo.view.familia import crear_familia_ajax, generos_por_familia_ajax, crear_genero_ajax
from apps.catalogo.view.serpiente import especie_por_genero_ajax, especie_crear_ajax
from apps.catalogo.view.anfibio import especie_por_genero_ajax as anfibio_especie_por_genero_ajax, especie_crear_ajax as anfibio_especie_crear_ajax
from apps.catalogo.view.saurio import especie_por_genero_ajax as saurio_especie_por_genero_ajax, especie_crear_ajax as saurio_especie_crear_ajax

app_name = 'catalogo'

urlpatterns = [
    # URL principal
    path('', HomeViews.as_view(), name="home"),
    
    # URL de búsqueda
    path('buscar/', BusquedaView.as_view(), name="buscar"),

    # URLs para CRUD Familia
    path('familia/', login_required(FamiliaListView.as_view()), name="familia-list"),
    path('familia/crear-ajax/', crear_familia_ajax, name='familia-crear-ajax'),
    path('familia/generos-ajax/', generos_por_familia_ajax, name='familia-generos-ajax'),
    path('genero/crear-ajax/', crear_genero_ajax, name='genero-crear-ajax'),
    
    # URLs para CRUD Serpientes
    path('serpiente/', login_required(SerpientesListView.as_view()), name="serpiente-list"),
    path('serpiente/crear/', login_required(SerpientesCreateView.as_view()), name="serpiente-create"),
    path('serpiente/<int:pk>/', login_required(SerpientesDetailView.as_view()), name="serpiente-detail"),
    path('serpiente/<int:pk>/editar/', login_required(SerpientesUpdateView.as_view()), name="serpiente-update"),
    path('serpiente/<int:pk>/eliminar/', login_required(SerpientesDeleteView.as_view()), name="serpiente-delete"),
    path('especie-por-genero-ajax/', especie_por_genero_ajax, name='especie-por-genero-ajax'),
    path('especie-crear-ajax/', especie_crear_ajax, name='especie-crear-ajax'),
    
    # URLs para CRUD Anfibios
    path('anfibio/', login_required(AnfibiosListView.as_view()), name="anfibio-list"),
    path('anfibio/crear/', login_required(AnfibiosCreateView.as_view()), name="anfibio-create"),
    path('anfibio/<int:pk>/', login_required(AnfibiosDetailView.as_view()), name="anfibio-detail"),
    path('anfibio/<int:pk>/editar/', login_required(AnfibiosUpdateView.as_view()), name="anfibio-update"),
    path('anfibio/<int:pk>/eliminar/', login_required(AnfibiosDeleteView.as_view()), name="anfibio-delete"),
    path('anfibio/especie-por-genero-ajax/', anfibio_especie_por_genero_ajax, name='anfibio-especie-por-genero-ajax'),
    path('anfibio/especie-crear-ajax/', anfibio_especie_crear_ajax, name='anfibio-especie-crear-ajax'),
    
    # URLs para CRUD Saurios
    path('saurio/', login_required(SauriosListView.as_view()), name="saurio-list"),
    path('saurio/crear/', login_required(SauriosCreateView.as_view()), name="saurio-create"),
    path('saurio/<int:pk>/', login_required(SauriosDetailView.as_view()), name="saurio-detail"),
    path('saurio/<int:pk>/editar/', login_required(SauriosUpdateView.as_view()), name="saurio-update"),
    path('saurio/<int:pk>/eliminar/', login_required(SauriosDeleteView.as_view()), name="saurio-delete"),
    path('saurio/especie-por-genero-ajax/', saurio_especie_por_genero_ajax, name='saurio-especie-por-genero-ajax'),
    path('saurio/especie-crear-ajax/', saurio_especie_crear_ajax, name='saurio-especie-crear-ajax'),
    
    path('prueba/', prueba, name='prueba'),
]
