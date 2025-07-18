// Funciones para manejar modales AJAX para crear familia, género y especie
// Compatible con serpientes, anfibios y saurios

function openFamiliaModal() {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold mb-4">Crear Nueva Familia</h3>
            <form id="familiaForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Nombre de la Familia</label>
                    <input type="text" id="familiaNombre" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Descripción</label>
                    <textarea id="familiaDescripcion" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="closeModal(this)" class="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Crear</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
    
    document.getElementById('familiaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createFamilia();
    });
}

function openGeneroModal() {
    const familiaSelect = document.getElementById('id_familia');
    const familiaId = familiaSelect.value;
    
    if (!familiaId) {
        alert('Por favor selecciona una familia primero');
        return;
    }
    
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold mb-4">Crear Nuevo Género</h3>
            <form id="generoForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Nombre del Género</label>
                    <input type="text" id="generoNombre" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Descripción</label>
                    <textarea id="generoDescripcion" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="closeModal(this)" class="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Crear</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
    
    document.getElementById('generoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createGenero(familiaId);
    });
}

function openEspecieModal() {
    const generoSelect = document.getElementById('id_genero');
    const generoId = generoSelect.value;
    
    if (!generoId) {
        alert('Por favor selecciona un género primero');
        return;
    }
    
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold mb-4">Crear Nueva Especie</h3>
            <form id="especieForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Nombre de la Especie</label>
                    <input type="text" id="especieNombre" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-2">Descripción</label>
                    <textarea id="especieDescripcion" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" rows="3"></textarea>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="closeModal(this)" class="px-4 py-2 text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Crear</button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
    
    document.getElementById('especieForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createEspecie(generoId);
    });
}

function closeModal(button) {
    const modal = button.closest('.fixed');
    modal.remove();
}

function createFamilia() {
    const nombre = document.getElementById('familiaNombre').value;
    const descripcion = document.getElementById('familiaDescripcion').value;
    
    fetch('/catalogo/api/familia/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            nombre: nombre,
            descripcion: descripcion
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el select de familia
            const familiaSelect = document.getElementById('id_familia');
            const option = new Option(data.familia.nombre, data.familia.id);
            familiaSelect.add(option);
            familiaSelect.value = data.familia.id;
            
            // Cerrar modal
            closeModal(document.querySelector('.fixed'));
            
            // Mostrar mensaje de éxito
            showMessage('Familia creada exitosamente', 'success');
        } else {
            showMessage('Error al crear la familia: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error al crear la familia', 'error');
    });
}

function createGenero(familiaId) {
    const nombre = document.getElementById('generoNombre').value;
    const descripcion = document.getElementById('generoDescripcion').value;
    
    fetch('/catalogo/api/genero/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            nombre: nombre,
            descripcion: descripcion,
            familia_id: familiaId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el select de género
            const generoSelect = document.getElementById('id_genero');
            const option = new Option(data.genero.nombre, data.genero.id);
            generoSelect.add(option);
            generoSelect.value = data.genero.id;
            
            // Cerrar modal
            closeModal(document.querySelector('.fixed'));
            
            // Mostrar mensaje de éxito
            showMessage('Género creado exitosamente', 'success');
        } else {
            showMessage('Error al crear el género: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error al crear el género', 'error');
    });
}

function createEspecie(generoId) {
    const nombre = document.getElementById('especieNombre').value;
    const descripcion = document.getElementById('especieDescripcion').value;
    
    fetch('/catalogo/api/especie/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            nombre: nombre,
            descripcion: descripcion,
            genero_id: generoId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar el select de especie
            const especieSelect = document.getElementById('id_especie');
            const option = new Option(data.especie.nombre, data.especie.id);
            especieSelect.add(option);
            especieSelect.value = data.especie.id;
            
            // Cerrar modal
            closeModal(document.querySelector('.fixed'));
            
            // Mostrar mensaje de éxito
            showMessage('Especie creada exitosamente', 'success');
        } else {
            showMessage('Error al crear la especie: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error al crear la especie', 'error');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    }`;
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Función para filtrar géneros cuando cambia la familia
function filterGeneros() {
    const familiaSelect = document.getElementById('id_familia');
    const generoSelect = document.getElementById('id_genero');
    const especieSelect = document.getElementById('id_especie');
    const familiaId = familiaSelect.value;
    
    // Limpiar géneros y especies
    generoSelect.innerHTML = '<option value="">---------</option>';
    especieSelect.innerHTML = '<option value="">---------</option>';
    
    if (familiaId) {
        fetch(`/catalogo/api/generos/${familiaId}/`)
            .then(response => response.json())
            .then(data => {
                data.generos.forEach(genero => {
                    const option = new Option(genero.nombre, genero.id);
                    generoSelect.add(option);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

// Función para filtrar especies cuando cambia el género
function filterEspecies() {
    const generoSelect = document.getElementById('id_genero');
    const especieSelect = document.getElementById('id_especie');
    const generoId = generoSelect.value;
    
    // Limpiar especies
    especieSelect.innerHTML = '<option value="">---------</option>';
    
    if (generoId) {
        fetch(`/catalogo/api/especies/${generoId}/`)
            .then(response => response.json())
            .then(data => {
                data.especies.forEach(especie => {
                    const option = new Option(especie.nombre, especie.id);
                    especieSelect.add(option);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

// Inicializar eventos cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const familiaSelect = document.getElementById('id_familia');
    const generoSelect = document.getElementById('id_genero');
    
    if (familiaSelect) {
        familiaSelect.addEventListener('change', filterGeneros);
    }
    
    if (generoSelect) {
        generoSelect.addEventListener('change', filterEspecies);
    }
}); 