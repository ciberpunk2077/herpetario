#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herpetario.settings')
django.setup()

from django.db import connection

# Eliminar todas las tablas de catalogo
with connection.cursor() as cursor:
    # Deshabilitar restricciones de clave foránea temporalmente
    cursor.execute("SET session_replication_role = replica;")
    
    # Eliminar tablas en orden correcto (dependencias)
    tables_to_drop = [
        'catalogo_atributoespecie',
        'catalogo_especie', 
        'catalogo_genero',
        'catalogo_familia',
        'catalogo_serpientes',
        'catalogo_user_user_permissions',
        'catalogo_user_groups',
        'catalogo_user'
    ]
    
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"Tabla {table} eliminada.")
        except Exception as e:
            print(f"No se pudo eliminar {table}: {e}")
    
    # Rehabilitar restricciones
    cursor.execute("SET session_replication_role = DEFAULT;")

print("Todas las tablas de catalogo han sido eliminadas.")
print("Ahora puedes ejecutar: python manage.py migrate catalogo") 