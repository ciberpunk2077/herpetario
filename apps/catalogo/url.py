from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.catalogo.views import *
from apps.catalogo.view.familia import *
from apps.catalogo.view.serpiente import *
app_name = 'catalogo'

urlpatterns = [
    # URL principal
    path('', HomeViews.as_view(), name="home"),

    # URLs para CRUD Familia
    path('familia/', login_required(FamiliaListView.as_view()), name="familia-list"),
    
    # URLs para CRUD Serpientes
    path('serpiente/', login_required(SerpientesListView.as_view()), name="serpiente-list"),
    path('serpiente/crear/', login_required(SerpientesCreateView.as_view()), name="serpiente-create"),
    path('serpiente/<int:pk>/', login_required(SerpientesDetailView.as_view()), name="serpiente-detail"),
    path('serpiente/<int:pk>/editar/', login_required(SerpientesUpdateView.as_view()), name="serpiente-update"),
    path('serpiente/<int:pk>/eliminar/', login_required(SerpientesDeleteView.as_view()), name="serpiente-delete"),
    
    path('prueba/', prueba, name='prueba'),
]
