# Estructura de Archivos JavaScript

Este directorio contiene todos los archivos JavaScript del proyecto, organizados de manera modular para mejor mantenimiento y control.

## Estructura de Archivos

```
static/js/
├── utils.js                    # Utilidades generales y funciones helper
├── forms.js                    # Funcionalidades específicas de formularios
├── charts/
│   └── dashboard-charts.js     # Clase principal para las gráficas del dashboard
└── README.md                   # Este archivo de documentación
```

## Descripción de Archivos

### `utils.js`
- **Propósito**: Funciones utilitarias generales
- **Funcionalidades**:
  - Validaciones comunes
  - Funciones de formato
  - Helpers para manipulación del DOM
- **Uso**: Se carga en todas las páginas que requieren funcionalidades básicas

### `forms.js`
- **Propósito**: Funcionalidades específicas para formularios
- **Funcionalidades**:
  - Validaciones de formularios
  - Manejo de envío de datos
  - Efectos visuales en campos
- **Uso**: Se carga en páginas con formularios

### `charts/dashboard-charts.js`
- **Propósito**: Gráficas interactivas para el dashboard principal
- **Funcionalidades**:
  - Gráfica de círculos (Pie Chart) para tipos de animales
  - Gráfica de dona (Doughnut Chart) para serpientes por subtipo
  - Gráfica de barras para especies en peligro de extinción
  - Efectos de hover en tarjetas de estadísticas
- **Dependencias**: Chart.js
- **Uso**: Se carga en la página principal (main.html)

## Inicialización de Gráficas

Las gráficas se inicializan directamente en el template `main.html` con el siguiente código:

```javascript
// Datos del servidor pasados desde Django
const chartData = {
    totalSerpientes: {{ total_serpientes|default:0 }},
    totalAnfibios: {{ total_anfibios|default:0 }},
    totalSaurios: {{ total_saurios|default:0 }},
    // ... más datos
};

// Inicializar las gráficas
window.dashboardCharts = new DashboardCharts(chartData);
```

## Orden de Carga

En el template `main.html`, los scripts se cargan en este orden:

1. `Chart.js` (CDN)
2. `utils.js`
3. `dashboard-charts.js`
4. Script de inicialización (inline en el template)

## Clase DashboardCharts

### Métodos Principales

- `constructor(data)`: Inicializa la clase con los datos del servidor
- `init()`: Crea todas las gráficas
- `createPieChart()`: Gráfica de círculos para tipos de animales
- `createSerpientesPieChart()`: Gráfica de dona para serpientes por subtipo
- `createEspeciesPeligroChart()`: Gráfica de barras para especies en peligro
- `addCardHoverEffects()`: Efectos de hover en tarjetas
- `destroy()`: Destruye todas las gráficas
- `updateData(newData)`: Actualiza datos y recrea gráficas

### Ejemplo de Uso

```javascript
// Crear instancia
const charts = new DashboardCharts(chartData);

// Actualizar datos
charts.updateData({
    totalSerpientes: 25,
    totalAnfibios: 15
});

// Destruir gráficas
charts.destroy();
```

## Ventajas de esta Estructura

1. **Modularidad**: Cada archivo tiene una responsabilidad específica
2. **Mantenibilidad**: Código organizado y fácil de mantener
3. **Reutilización**: Funciones que se pueden usar en múltiples páginas
4. **Control**: Mejor control sobre qué código se carga en cada página
5. **Debugging**: Más fácil identificar y corregir problemas

## Notas de Desarrollo

- Todos los archivos JavaScript usan ES6+ syntax
- Se incluyen comentarios descriptivos para facilitar el mantenimiento
- Las gráficas son responsivas y se adaptan a diferentes tamaños de pantalla
- Se incluyen logs de debug para facilitar el desarrollo 