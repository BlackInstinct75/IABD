/**
 * AutoDoc - Frontend Logic
 * Gestión de la interfaz y comunicación con el backend
 */

// Estado global de la aplicación
let currentCar = null;
let allCars = [];
let lastSavedDraft = '';

// Referencias a elementos del DOM
const elements = {
    carList: document.getElementById('carList'),
    carDetail: document.getElementById('carDetail'),
    emptyState: document.getElementById('emptyState'),
    detailContent: document.getElementById('detailContent'),
    carImage: document.getElementById('carImage'),
    carTitle: document.getElementById('carTitle'),
    carPlate: document.getElementById('carPlate'),
    draftTextarea: document.getElementById('draftTextarea'),
    saveDraftBtn: document.getElementById('saveDraftBtn'),
    saveMessage: document.getElementById('saveMessage'),
    generateBtn: document.getElementById('generateBtn'),
    aiResult: document.getElementById('aiResult'),
    aiDescription: document.getElementById('aiDescription'),
    aiMessage: document.getElementById('aiMessage'),
    copyBtn: document.getElementById('copyBtn'),
    searchInput: document.getElementById('searchInput'),
    importFile: document.getElementById('importFile')
};

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadCars();
    setupEventListeners();
});

function setupEventListeners() {
    // Guardar borrador
    elements.saveDraftBtn.addEventListener('click', saveDraft);

    // Generar descripción con IA
    if (elements.generateBtn) {
        elements.generateBtn.addEventListener('click', generateDescription);
    }

    // Copiar descripción
    if (elements.copyBtn) {
        elements.copyBtn.addEventListener('click', copyDescription);
    }

    // Buscar coches
    if (elements.searchInput) {
        elements.searchInput.addEventListener('input', filterCars);
    }

    // Importar coche
    elements.importFile.addEventListener('change', importCar);

    // Detectar cambios en el textarea para habilitar/deshabilitar botón IA
    if (elements.generateBtn) {
        elements.draftTextarea.addEventListener('input', updateGenerateButton);
    }

    // Detectar cambios en el textarea para habilitar el botón de guardar
    elements.draftTextarea.addEventListener('input', updateSaveButton);
}

// ============================================
// API CALLS
// ============================================

async function loadCars() {
    try {
        const response = await fetch('/api/cars');
        if (!response.ok) throw new Error('Error cargando coches');

        allCars = await response.json();
        renderCarList(allCars);

    } catch (error) {
        console.error('Error:', error);
        elements.carList.innerHTML = `
            <div class="error-message">
                <p>❌ Error cargando la lista de coches</p>
                <p class="error-detail">${error.message}</p>
            </div>
        `;
    }
}

async function loadCarDetail(plate) {
    try {
        const response = await fetch(`/api/cars/${plate}`);
        if (!response.ok) throw new Error('Error cargando detalles del coche');

        currentCar = await response.json();
        renderCarDetail(currentCar);

    } catch (error) {
        console.error('Error:', error);
        showMessage(elements.aiMessage, `Error: ${error.message}`, 'error');
    }
}

async function saveDraft() {
    if (!currentCar) return;

    const draft = elements.draftTextarea.value;

    try {
        elements.saveDraftBtn.disabled = true;
        elements.saveDraftBtn.textContent = 'Guardando...';

        const response = await fetch(`/api/cars/${currentCar.plate}/draft`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draft })
        });

        if (!response.ok) throw new Error('Error guardando borrador');

        const result = await response.json();

        // Actualizar estado
        currentCar.draft = draft;
        currentCar.hasDraft = draft.trim().length > 0;
        lastSavedDraft = draft;

        // Actualizar lista de coches
        const carIndex = allCars.findIndex(c => c.plate === currentCar.plate);
        if (carIndex !== -1) {
            allCars[carIndex] = currentCar;
            renderCarList(allCars);
        }

        showToast('Registro guardado ✅');
        updateGenerateButton();
        updateSaveButton();

    } catch (error) {
        console.error('Error:', error);
        showMessage(elements.saveMessage, `Error: ${error.message}`, 'error');
    } finally {
        elements.saveDraftBtn.innerHTML = `
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path>
            </svg>
            Guardar
        `;
    }
}

async function generateDescription() {
    if (!currentCar || !elements.draftTextarea.value.trim()) {
        showMessage(elements.aiMessage, 'Añade un borrador antes de generar', 'warning');
        return;
    }

    const draft = elements.draftTextarea.value;

    try {
        elements.generateBtn.disabled = true;
        elements.generateBtn.textContent = 'Generando...';
        elements.aiResult.style.display = 'none';

        const response = await fetch(`/api/cars/${currentCar.plate}/generate-description`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draft })
        });

        const result = await response.json();

        if (!response.ok) {
            // Error 501: Funcionalidad no implementada
            if (response.status === 501) {
                showMessage(
                    elements.aiMessage,
                    '⚠️ Funcionalidad pendiente de implementación. El alumnado debe completar ai_service.py',
                    'warning'
                );
            } else {
                throw new Error(result.detail || 'Error generando descripción');
            }
        } else {
            // Éxito
            elements.aiDescription.textContent = result.description;
            elements.aiResult.style.display = 'block';
            showMessage(elements.aiMessage, '✅ Descripción generada correctamente', 'success');
        }

    } catch (error) {
        console.error('Error:', error);
        showMessage(elements.aiMessage, `Error: ${error.message}`, 'error');
    } finally {
        elements.generateBtn.disabled = false;
        elements.generateBtn.innerHTML = `
            <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Generar descripción técnica (IA)
        `;
    }
}

async function importCar(event) {
    const file = event.target.files[0];
    if (!file) return;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/cars/import', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || 'Error importando coche');
        }

        // Recargar lista
        await loadCars();

        // Mostrar mensaje de éxito
        showMessage(elements.saveMessage, result.message, 'success');

        // Seleccionar el coche recién importado
        loadCarDetail(result.car.plate);

    } catch (error) {
        console.error('Error:', error);
        alert(`Error importando coche: ${error.message}`);
    } finally {
        // Limpiar input file
        event.target.value = '';
    }
}

// ============================================
// RENDER FUNCTIONS
// ============================================

function renderCarList(cars) {
    if (cars.length === 0) {
        elements.carList.innerHTML = `
            <div class="empty-list">
                <p>No hay coches disponibles</p>
                <p class="empty-hint">Añade uno usando el botón "Añadir coche"</p>
            </div>
        `;
        return;
    }

    elements.carList.innerHTML = cars.map(car => `
        <div class="car-card ${currentCar?.plate === car.plate ? 'active' : ''}"
             data-plate="${car.plate}"
             onclick="selectCar('${car.plate}')">
            <img
                src="${car.imageURL || '/data/images/placeholder.jpg'}"
                alt="${car.title}"
                class="car-thumbnail"
                onerror="this.src='/data/images/placeholder.jpg'"
            >
            <div class="car-card-info">
                <p class="car-card-title">${car.title}</p>
                <p class="car-card-plate">${car.plate}</p>
            </div>
            <span class="car-status ${car.hasDraft ? 'has-draft' : 'no-draft'}">
                ${car.hasDraft ? 'Completado' : 'Pendiente'}
            </span>
        </div>
    `).join('');
}

function renderCarDetail(car) {
    // Ocultar empty state, mostrar detalle
    elements.emptyState.style.display = 'none';
    elements.detailContent.style.display = 'block';

    // Actualizar contenido
    elements.carImage.src = car.imageURL || '/data/images/placeholder.jpg';
    elements.carImage.onerror = () => {
        elements.carImage.src = '/data/images/placeholder.jpg';
    };
    elements.carTitle.textContent = car.title;
    elements.carPlate.textContent = `Matrícula: ${car.plate}`;
    elements.draftTextarea.value = car.draft || '';
    lastSavedDraft = car.draft || '';

    // Limpiar mensajes y resultados previos
    elements.saveMessage.style.display = 'none';
    if (elements.aiMessage) {
        elements.aiMessage.style.display = 'none';
    }
    if (elements.aiResult) {
        elements.aiResult.style.display = 'none';
    }

    // Actualizar estado de los botones
    updateGenerateButton();
    updateSaveButton();

    // Resaltar coche seleccionado en la lista
    renderCarList(allCars);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function selectCar(plate) {
    loadCarDetail(plate);
}

function updateGenerateButton() {
    if (!elements.generateBtn) return;

    const hasDraft = elements.draftTextarea.value.trim().length > 0;
    elements.generateBtn.disabled = !hasDraft;

    if (!hasDraft) {
        elements.generateBtn.title = 'Añade un borrador antes de generar';
    } else {
        elements.generateBtn.title = 'Generar descripción técnica usando IA';
    }
}

function updateSaveButton() {
    const currentDraft = elements.draftTextarea.value;
    const hasChanges = currentDraft !== lastSavedDraft;

    elements.saveDraftBtn.disabled = !hasChanges;

    if (!hasChanges) {
        elements.saveDraftBtn.title = 'No hay cambios por guardar';
    } else {
        elements.saveDraftBtn.title = 'Guardar cambios';
    }
}

function filterCars() {
    if (!elements.searchInput) return;

    const query = elements.searchInput.value.toLowerCase().trim();

    if (!query) {
        renderCarList(allCars);
        return;
    }

    const filtered = allCars.filter(car =>
        car.title.toLowerCase().includes(query) ||
        car.plate.toLowerCase().includes(query)
    );

    renderCarList(filtered);
}

function copyDescription() {
    const text = elements.aiDescription.textContent;

    navigator.clipboard.writeText(text)
        .then(() => {
            showMessage(elements.aiMessage, '📋 Descripción copiada al portapapeles', 'success');
        })
        .catch(err => {
            console.error('Error copiando:', err);
            showMessage(elements.aiMessage, 'Error copiando al portapapeles', 'error');
        });
}

function showMessage(element, text, type = 'info') {
    element.textContent = text;
    element.className = `message message-${type}`;
    element.style.display = 'block';

    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

function showToast(message, type = 'success') {
    // Crear elemento toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Agregar al body
    document.body.appendChild(toast);

    // Mostrar con animación
    setTimeout(() => toast.classList.add('show'), 10);

    // Ocultar y eliminar después de 3 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============================================
// GLOBAL FUNCTIONS (called from HTML)
// ============================================

// Hacer selectCar accesible globalmente
window.selectCar = selectCar;
