"""herpetario URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.catalogo.views import prueba
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.shortcuts import redirect

from herpetario import settings


urlpatterns = [
                  path('', lambda request: redirect('catalogo:home'), name="home"),
                  path('admin/', admin.site.urls),
                  path('login/', views.LoginView.as_view(), name="login"),
                  path('logout/', views.LogoutView.as_view(), name="logout"),
                  path('catalogo/', include('apps.catalogo.url', namespace='catalogo')),
                  path('info/', include('info.urls', namespace='info')),
                 

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
