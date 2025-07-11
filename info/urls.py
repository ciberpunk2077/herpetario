from django.urls import path
from .views import *

app_name = 'info'

urlpatterns = [
    # URL principal
    path('', HomeViews.as_view(), name="home"),

    # URLs para páginas de información
    path('presentacion/', presentacion, name="presentacion"),
    path('coleccion/', coleccion, name='coleccion'),
    path('investigacion/', investigacion, name='investigacion'),
    path('personal/', personal, name='personal'),
]
