// Dashboard Charts Initialization
// Este archivo inicializa las gráficas del dashboard del herpetario

class DashboardInitializer {
    constructor() {
        this.chartData = null;
        this.dashboardCharts = null;
    }

    // Método para configurar los datos desde el template
    setChartData(data) {
        this.chartData = data;
        console.log('Datos de las gráficas configurados:', this.chartData);
    }

    // Método para inicializar las gráficas
    initialize() {
        // Verificar que Chart.js esté disponible
        if (typeof Chart === 'undefined') {
            console.error('Chart.js no está cargado. Asegúrate de incluir la librería antes de este script.');
            return;
        }

        // Verificar que DashboardCharts esté disponible
        if (typeof DashboardCharts === 'undefined') {
            console.error('DashboardCharts no está cargado. Asegúrate de incluir dashboard-charts.js antes de este script.');
            return;
        }

        // Verificar que los datos estén configurados
        if (!this.chartData) {
            console.error('Los datos de las gráficas no están configurados. Llama a setChartData() primero.');
            return;
        }

        // Inicializar las gráficas
        try {
            this.dashboardCharts = new DashboardCharts(this.chartData);
            console.log('Gráficas del dashboard inicializadas correctamente');
        } catch (error) {
            console.error('Error al inicializar las gráficas:', error);
        }
    }

    // Método para reinicializar las gráficas (útil para actualizaciones dinámicas)
    reinitialize(newData = null) {
        if (newData) {
            this.setChartData(newData);
        }
        this.initialize();
    }
}

// Crear instancia global
window.dashboardInitializer = new DashboardInitializer();

// Auto-inicializar cuando el DOM esté listo (si los datos ya están configurados)
document.addEventListener('DOMContentLoaded', function() {
    if (window.dashboardInitializer.chartData) {
        window.dashboardInitializer.initialize();
    }
}); 