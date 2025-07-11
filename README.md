# 🐍 Nexus Herpetario

Sistema de gestión de catálogo de serpientes y especies herpetológicas desarrollado con Django.

## 📋 Descripción

Nexus Herpetario es una aplicación web moderna para la gestión y catalogación de especies de serpientes, con un enfoque en la conservación y educación. El sistema permite registrar, gestionar y consultar información detallada sobre diferentes especies de serpientes.

## ✨ Características

- **🐍 Catálogo de Serpientes**: Gestión completa de especies con información taxonómica
- **🎨 Interfaz Moderna**: Diseño responsivo con Tailwind CSS
- **🔐 Sistema de Autenticación**: Login/logout con sesiones seguras
- **📊 CRUD Completo**: Crear, leer, actualizar y eliminar registros
- **🔍 Búsqueda Inteligente**: Filtros y búsqueda en tiempo real
- **📱 Responsive Design**: Optimizado para móviles y tablets
- **🎯 UX Intuitiva**: Navegación fluida y confirmaciones visuales

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.21
- **Frontend**: Tailwind CSS, HTML5, JavaScript
- **Base de Datos**: PostgreSQL
- **Autenticación**: Django Auth System
- **Iconos**: SVG Icons
- **Deployment**: Ready for production

## 🚀 Instalación

### Prerrequisitos

- Python 3.10+
- PostgreSQL
- Node.js (para Tailwind CSS)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/nexus-herpetario.git
   cd nexus-herpetario
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv virtual
   virtual\Scripts\activate  # Windows
   # source virtual/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos PostgreSQL
   - Configurar credenciales en `herpetario/settings.py`

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Crear datos de prueba (opcional)**
   ```bash
   python manage.py crear_datos_prueba
   ```

8. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## 📁 Estructura del Proyecto

```
herpetario/
├── apps/
│   └── catalogo/           # App principal del catálogo
│       ├── models.py       # Modelos de datos
│       ├── views.py        # Vistas y lógica
│       ├── forms.py        # Formularios
│       └── templates/      # Plantillas HTML
├── info/                   # App de información general
├── templates/              # Plantillas base
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos
└── herpetario/            # Configuración principal
    ├── settings.py        # Configuración Django
    └── urls.py           # URLs principales
```

## 🎯 Funcionalidades Principales

### Gestión de Serpientes
- **Lista de Serpientes**: Vista en grid con tarjetas interactivas
- **Detalle de Serpiente**: Información completa con badges de estado
- **Crear Serpiente**: Formulario intuitivo con validación
- **Editar Serpiente**: Modificación de datos existentes
- **Eliminar Serpiente**: Confirmación antes de eliminar

### Información Taxonómica
- **Género**: Clasificación taxonómica
- **Familia**: Agrupación científica
- **Nombre Científico**: Nomenclatura binomial
- **Nombre Común**: Denominación popular

### Estados de Conservación
- **En Peligro**: Marcado para especies amenazadas
- **Subtipo**: Venenosa, Constrictora, No venenosa
- **Hábitat**: Información del entorno natural

## 🔧 Configuración

### Variables de Entorno

Crear archivo `secret.json` en la raíz del proyecto:

```json
{
    "DB_NAME": "herpetario",
    "DB_USER": "tu_usuario",
    "DB_PASSWORD": "tu_password",
    "DB_HOST": "localhost",
    "DB_PORT": "5432"
}
```

### Base de Datos

El proyecto está configurado para PostgreSQL. Asegúrate de:
- Tener PostgreSQL instalado
- Crear la base de datos `herpetario`
- Configurar las credenciales correctas

## 🎨 Personalización

### Colores del Tema

Los colores principales están definidos en `templates/base.html`:

- **Primary**: #2A9D8F (Verde azulado)
- **Secondary**: #264653 (Azul oscuro)
- **Accent**: #E9C46A (Amarillo)
- **Danger**: #E76F51 (Naranja rojizo)

### Estilos

El proyecto usa Tailwind CSS para estilos. Los archivos principales están en:
- `templates/base.html` - Configuración de Tailwind
- `static/css/` - Estilos personalizados

## 🚀 Deployment

### Producción

1. **Configurar variables de entorno**
2. **Configurar base de datos de producción**
3. **Ejecutar `python manage.py collectstatic`**
4. **Configurar servidor web (Nginx/Apache)**
5. **Configurar WSGI (Gunicorn/uWSGI)**

### Docker (Opcional)

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [TuUsuario](https://github.com/TuUsuario)

## 🙏 Agradecimientos

- Django Framework
- Tailwind CSS
- Comunidad de Python
- Herpetólogos y conservacionistas

## 📞 Contacto

- **Email**: tu-email@ejemplo.com
- **GitHub**: [@TuUsuario](https://github.com/TuUsuario)
- **LinkedIn**: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

**¡Gracias por usar Nexus Herpetario! 🐍✨** 