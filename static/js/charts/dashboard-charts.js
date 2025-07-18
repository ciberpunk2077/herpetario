/**
 * Dashboard Charts - Gráficas para el dashboard principal
 * Maneja las gráficas de estadísticas del catálogo de especies
 */

class DashboardCharts {
    constructor(data) {
        this.data = data;
        this.charts = {};
        this.init();
    }

    init() {
        this.createPieChart();
        this.createSerpientesPieChart();
        this.createEspeciesPeligroChart();
        this.addCardHoverEffects();
    }

    /**
     * Gráfica de círculos para tipos de animales
     */
    createPieChart() {
        const pieChartCtx = document.getElementById('pieChart');
        if (!pieChartCtx) {
            console.error('No se encontró el elemento pieChart');
            return;
        }

        console.log('Creando gráfica de tipos de animales...');
        this.charts.pieChart = new Chart(pieChartCtx, {
            type: 'pie',
            data: {
                labels: ['Serpientes', 'Anfibios', 'Saurios'],
                datasets: [{
                    data: [
                        this.data.totalSerpientes || 0,
                        this.data.totalAnfibios || 0,
                        this.data.totalSaurios || 0
                    ],
                    backgroundColor: [
                        '#ef4444', // red-500
                        '#10b981', // green-500
                        '#3b82f6'  // blue-500
                    ],
                    borderColor: [
                        '#dc2626', // red-600
                        '#059669', // green-600
                        '#2563eb'  // blue-600
                    ],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            }
        });
    }

    /**
     * Gráfica de dona para serpientes por subtipo
     */
    createSerpientesPieChart() {
        const serpientesPieChartCtx = document.getElementById('serpientesPieChart');
        if (!serpientesPieChartCtx) {
            console.error('No se encontró el elemento serpientesPieChart');
            return;
        }

        console.log('Creando gráfica de serpientes por subtipo...');
        this.charts.serpientesPieChart = new Chart(serpientesPieChartCtx, {
            type: 'doughnut',
            data: {
                labels: ['Venenosas', 'No venenosas', 'Constrictoras'],
                datasets: [{
                    data: [
                        this.data.serpientesVenenosas || 0,
                        this.data.serpientesNoVenenosas || 0,
                        this.data.serpientesConstrictoras || 0
                    ],
                    backgroundColor: [
                        '#dc2626', // red-600
                        '#059669', // green-600
                        '#9333ea'  // purple-600
                    ],
                    borderColor: [
                        '#b91c1c', // red-700
                        '#047857', // green-700
                        '#7c3aed'  // purple-700
                    ],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                },
                cutout: '60%'
            }
        });
    }

    /**
     * Gráfica de barras para especies en peligro
     */
    createEspeciesPeligroChart() {
        const stackedAreaChartCtx = document.getElementById('stackedAreaChart');
        if (!stackedAreaChartCtx) {
            console.error('No se encontró el elemento stackedAreaChart');
            return;
        }

        console.log('Creando gráfica de especies en peligro...');
        this.charts.stackedAreaChart = new Chart(stackedAreaChartCtx, {
            type: 'bar',
            data: {
                labels: ['Serpientes', 'Anfibios', 'Saurios'],
                datasets: [
                    {
                        label: 'Especies en Peligro de Extinción',
                        data: [
                            this.data.serpientesEnPeligroCount || 0,
                            this.data.anfibiosEnPeligroCount || 0,
                            this.data.sauriosEnPeligroCount || 0
                        ],
                        backgroundColor: [
                            '#ef4444', // red-500 para serpientes
                            '#10b981', // green-500 para anfibios
                            '#3b82f6'  // blue-500 para saurios
                        ],
                        borderColor: [
                            '#dc2626', // red-600
                            '#059669', // green-600
                            '#2563eb'  // blue-600
                        ],
                        borderWidth: 2,
                        borderRadius: 8,
                        borderSkipped: false,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#dc2626',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.parsed.y || 0;
                                return `${label}: ${value} especies`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Tipos de Animales',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Número de Especies en Peligro',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            drawBorder: false
                        }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    /**
     * Efectos de hover para las tarjetas de estadísticas
     */
    addCardHoverEffects() {
        const statCards = document.querySelectorAll('.bg-white.rounded-xl.p-6.shadow-lg');
        statCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.transition = 'transform 0.3s ease';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    /**
     * Método para destruir todas las gráficas
     */
    destroy() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }

    /**
     * Método para actualizar datos de las gráficas
     */
    updateData(newData) {
        this.data = { ...this.data, ...newData };
        this.destroy();
        this.init();
    }
}

// Exportar la clase para uso global
window.DashboardCharts = DashboardCharts; 