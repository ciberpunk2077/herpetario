/**
 * Utilidades JavaScript generales para el proyecto Herpetario
 */

class HerpetarioUtils {
    /**
     * Formatear números con separadores de miles
     */
    static formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    /**
     * Calcular porcentaje
     */
    static calculatePercentage(value, total) {
        if (total === 0) return 0;
        return ((value / total) * 100).toFixed(1);
    }

    /**
     * Validar email
     */
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Mostrar notificación toast
     */
    static showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        // Configurar colores según el tipo
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-black',
            info: 'bg-blue-500 text-white'
        };
        
        toast.className += ` ${colors[type] || colors.info}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Animar entrada
        setTimeout(() => {
            toast.classList.remove('translate-x-full');
        }, 100);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }

    /**
     * Confirmar acción con modal
     */
    static confirmAction(message, callback) {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        modal.innerHTML = `
            <div class="bg-white rounded-lg p-6 max-w-md mx-4">
                <h3 class="text-lg font-bold mb-4">Confirmar acción</h3>
                <p class="text-gray-600 mb-6">${message}</p>
                <div class="flex justify-end space-x-3">
                    <button class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors" onclick="this.closest('.fixed').remove()">
                        Cancelar
                    </button>
                    <button class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors" onclick="this.closest('.fixed').remove(); if(typeof ${callback} === 'function') ${callback}()">
                        Confirmar
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    /**
     * Cargar imagen con fallback
     */
    static loadImageWithFallback(imgElement, fallbackSrc) {
        imgElement.onerror = function() {
            this.src = fallbackSrc;
            this.onerror = null; // Prevenir loop infinito
        };
    }

    /**
     * Debounce function para optimizar eventos
     */
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Throttle function para limitar frecuencia de eventos
     */
    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Copiar texto al portapapeles
     */
    static async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Texto copiado al portapapeles', 'success');
        } catch (err) {
            console.error('Error al copiar texto:', err);
            this.showToast('Error al copiar texto', 'error');
        }
    }

    /**
     * Generar ID único
     */
    static generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Formatear fecha
     */
    static formatDate(date, format = 'DD/MM/YYYY') {
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format
            .replace('DD', day)
            .replace('MM', month)
            .replace('YYYY', year);
    }

    /**
     * Validar formulario
     */
    static validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('border-red-500');
                isValid = false;
            } else {
                input.classList.remove('border-red-500');
            }
        });
        
        return isValid;
    }

    /**
     * Limpiar formulario
     */
    static clearForm(formElement) {
        const inputs = formElement.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.value = '';
            input.classList.remove('border-red-500');
        });
    }
}

// Exportar para uso global
window.HerpetarioUtils = HerpetarioUtils; 