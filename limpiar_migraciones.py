#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herpetario.settings')
django.setup()

from django.db import connection

# Limpiar el registro de migraciones de la app catalogo
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'catalogo';")
    print("Registro de migraciones de 'catalogo' limpiado exitosamente.")

print("Ahora puedes ejecutar: python manage.py migrate catalogo") 