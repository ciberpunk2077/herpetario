from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.catalogo.views import *
from apps.catalogo.view.familia import *
app_name = 'catalogos'

urlpatterns = [
    # URL principal
    path('', HomeViews.as_view(), name="home"),

    # URLs para CRUD Familia

    path('familia/', login_required(FamiliaListView.as_view()), name="familia-list"),


]
