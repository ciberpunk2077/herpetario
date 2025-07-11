#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'herpetario.settings')
django.setup()

from django.db import connection

# Verificar qué tablas existen
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'catalogo_%'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print("Tablas existentes de la app catalogo:")
    for table in tables:
        print(f"  - {table[0]}")
    
    if not tables:
        print("  No hay tablas de catalogo en la base de datos.") 