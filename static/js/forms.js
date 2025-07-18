/**
 * Manejo de formularios para el proyecto Herpetario
 */

class FormHandler {
    constructor(formSelector, options = {}) {
        this.form = document.querySelector(formSelector);
        this.options = {
            validateOnSubmit: true,
            showSuccessMessage: true,
            showErrorMessage: true,
            redirectOnSuccess: null,
            ...options
        };
        
        if (this.form) {
            this.init();
        } else {
            console.error(`Formulario no encontrado: ${formSelector}`);
        }
    }

    init() {
        this.bindEvents();
        this.setupValidation();
        this.setupAutoSave();
    }

    bindEvents() {
        // Evento de envío del formulario
        this.form.addEventListener('submit', (e) => {
            if (this.options.validateOnSubmit && !this.validateForm()) {
                e.preventDefault();
                return false;
            }
        });

        // Validación en tiempo real
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Auto-guardado
        if (this.options.autoSave) {
            inputs.forEach(input => {
                input.addEventListener('change', () => this.autoSave());
            });
        }
    }

    setupValidation() {
        // Agregar validaciones personalizadas
        this.validators = {
            required: (value) => value.trim() !== '',
            email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            minLength: (value, min) => value.length >= min,
            maxLength: (value, max) => value.length <= max,
            numeric: (value) => !isNaN(value) && value !== '',
            url: (value) => {
                try {
                    new URL(value);
                    return true;
                } catch {
                    return false;
                }
            }
        };
    }

    setupAutoSave() {
        if (this.options.autoSave) {
            this.autoSaveTimer = null;
            this.autoSaveDelay = this.options.autoSaveDelay || 2000;
        }
    }

    validateField(field) {
        const value = field.value;
        const rules = field.dataset.validation ? field.dataset.validation.split('|') : [];
        
        for (const rule of rules) {
            const [validatorName, param] = rule.split(':');
            
            if (this.validators[validatorName]) {
                const isValid = this.validators[validatorName](value, param);
                
                if (!isValid) {
                    this.showFieldError(field, this.getErrorMessage(validatorName, param));
                    return false;
                }
            }
        }
        
        this.clearFieldError(field);
        return true;
    }

    validateForm() {
        const fields = this.form.querySelectorAll('[data-validation]');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    showFieldError(field, message) {
        // Remover error anterior
        this.clearFieldError(field);
        
        // Agregar clase de error
        field.classList.add('border-red-500', 'focus:border-red-500');
        
        // Crear mensaje de error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-500 text-sm mt-1';
        errorDiv.textContent = message;
        errorDiv.id = `error-${field.id || field.name}`;
        
        // Insertar después del campo
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500', 'focus:border-red-500');
        
        const errorDiv = document.getElementById(`error-${field.id || field.name}`);
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    getErrorMessage(validatorName, param) {
        const messages = {
            required: 'Este campo es obligatorio',
            email: 'Ingresa un email válido',
            minLength: `Mínimo ${param} caracteres`,
            maxLength: `Máximo ${param} caracteres`,
            numeric: 'Solo se permiten números',
            url: 'Ingresa una URL válida'
        };
        
        return messages[validatorName] || 'Campo inválido';
    }

    autoSave() {
        if (!this.options.autoSave) return;
        
        clearTimeout(this.autoSaveTimer);
        this.autoSaveTimer = setTimeout(() => {
            this.saveFormData();
        }, this.autoSaveDelay);
    }

    saveFormData() {
        const formData = new FormData(this.form);
        const data = {};
        
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem(`form_${this.form.id || 'default'}`, JSON.stringify(data));
        console.log('Formulario guardado automáticamente');
    }

    loadFormData() {
        const savedData = localStorage.getItem(`form_${this.form.id || 'default'}`);
        
        if (savedData) {
            const data = JSON.parse(savedData);
            
            Object.keys(data).forEach(key => {
                const field = this.form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = data[key];
                }
            });
            
            console.log('Datos del formulario restaurados');
        }
    }

    clearForm() {
        this.form.reset();
        localStorage.removeItem(`form_${this.form.id || 'default'}`);
        
        // Limpiar errores
        const errorDivs = this.form.querySelectorAll('.text-red-500');
        errorDivs.forEach(div => div.remove());
        
        // Limpiar clases de error
        const fields = this.form.querySelectorAll('input, select, textarea');
        fields.forEach(field => {
            field.classList.remove('border-red-500', 'focus:border-red-500');
        });
    }

    submitForm() {
        if (this.validateForm()) {
            this.form.submit();
        }
    }

    // Método para manejar respuestas AJAX
    handleResponse(response, successCallback, errorCallback) {
        if (response.ok) {
            const data = response.json();
            
            if (this.options.showSuccessMessage) {
                HerpetarioUtils.showToast('Formulario enviado correctamente', 'success');
            }
            
            if (successCallback) {
                successCallback(data);
            }
            
            if (this.options.redirectOnSuccess) {
                window.location.href = this.options.redirectOnSuccess;
            }
        } else {
            if (this.options.showErrorMessage) {
                HerpetarioUtils.showToast('Error al enviar el formulario', 'error');
            }
            
            if (errorCallback) {
                errorCallback(response);
            }
        }
    }
}

// Clase específica para formularios de especies
class EspecieFormHandler extends FormHandler {
    constructor(formSelector, options = {}) {
        super(formSelector, {
            autoSave: true,
            autoSaveDelay: 3000,
            ...options
        });
    }

    setupValidation() {
        super.setupValidation();
        
        // Validaciones específicas para especies
        this.validators.nombreCientifico = (value) => {
            return /^[A-Z][a-z]+ [a-z]+$/.test(value);
        };
        
        this.validators.nombreComun = (value) => {
            return value.length >= 2 && value.length <= 100;
        };
    }

    getErrorMessage(validatorName, param) {
        const messages = {
            ...super.getErrorMessage(validatorName, param),
            nombreCientifico: 'El nombre científico debe tener el formato "Género especie"',
            nombreComun: 'El nombre común debe tener entre 2 y 100 caracteres'
        };
        
        return messages[validatorName] || 'Campo inválido';
    }
}

// Exportar clases para uso global
window.FormHandler = FormHandler;
window.EspecieFormHandler = EspecieFormHandler; 