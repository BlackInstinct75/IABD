# 🚗 AutoDoc - Gestor de Fichas de Intervención

## 📦 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `fastapi` - Framework web para el backend
- `uvicorn` - Servidor ASGI
- `python-multipart` - Para manejo de archivos

## 🚀 Uso

### Iniciar el servidor

```bash
python main.py
```

Deberías ver:

```
🚗 Iniciando servidor AutoDoc en http://localhost:8000
📁 Directorio de datos: /path/to/data
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Acceder a la aplicación

Abre tu navegador en: **http://localhost:8000**

### Funcionalidades disponibles

1. **Ver lista de coches**: En la columna izquierda verás los coches disponibles
2. **Seleccionar coche**: Haz clic en una carta para ver detalles
3. **Editar comentarios**: Escribe o modifica el texto del mecánico
4. **Guardar**: Pulsa "Guardar" para persistir cambios
5. **Añadir coche**: Usa el botón "Añadir coche" para importar un `.txt`

### Importar un coche nuevo

1. Crea un archivo `.txt` con el formato especificado [más abajo](#-formato-de-archivos-de-coche)
2. Haz clic en "Añadir coche"
3. Selecciona el archivo
4. El coche aparecerá automáticamente en la lista

## 📁 Estructura del Proyecto

```
completion-challenge/
├── README.md                    # Este archivo
├── main.py                      # Backend FastAPI (servidor)
├── requirements.txt             # Dependencias Python
│
├── data/
│   ├── cars/                    # Archivos de coches (*.txt)
│   │   ├── 1234ABC.txt         # Ejemplo 1: SEAT León
│   │   ├── 5678DEF.txt         # Ejemplo 2: Renault Clio
│   │   └── 9012GHI.txt         # Ejemplo 3: VW Golf
│   └── images/                  # Imágenes de coches
│
└── static/                      # Frontend
    ├── index.html              # Página principal
    ├── app.js                  # Lógica JavaScript
    └── styles.css              # Estilos CSS
```

## 🔌 API Endpoints

El backend expone los siguientes endpoints:

### `GET /api/cars`

Lista todos los coches disponibles.

**Respuesta:**
```json
[
  {
    "title": "SEAT León 1.6 TDI",
    "plate": "1234ABC",
    "imageURL": "/data/images/placeholder.jpg",
    "draft": "Cambio de correa...",
    "hasDraft": true
  }
]
```

### `GET /api/cars/{plate}`

Obtiene detalles de un coche específico.

**Ejemplo:** `GET /api/cars/1234ABC`

### `POST /api/cars/{plate}/draft`

Actualiza el borrador de un coche.

**Body:**
```json
{
  "draft": "Texto del borrador actualizado"
}
```

### `POST /api/cars/import`

Importa un nuevo coche desde un archivo `.txt`.

**Form Data:**
- `file`: Archivo `.txt` con formato válido

### `GET /health`

Endpoint de salud para verificar que el servidor funciona.

---

## 📄 Formato de Archivos de Coche

Los archivos de coche son archivos de texto plano (`.txt`) con el siguiente formato:

```
Title: <Nombre del vehículo>
Plate: <Matrícula>
ImageURL: <URL o ruta de imagen>
---
Draft:
<Borrador del mecánico (opcional)>
```

### Ejemplo válido

```txt
Title: SEAT León 1.6 TDI
Plate: 1234ABC
ImageURL: /data/images/placeholder.jpg
---
Draft:
Cambio de correa de distribución por desgaste. Ajuste de tensión. Prueba en vacío OK.
```

### Reglas

- **Campos obligatorios**: `Title` y `Plate` deben existir
- **Nombre del archivo**: Debe ser `<Plate>.txt` (ej: `1234ABC.txt`)
- **Separador**: La línea `---` separa metadatos del borrador
- **Draft vacío**: Si no hay borrador, omite todo después de `Draft:` o déjalo vacío

## 🎓 Tarea para el Alumnado

### Objetivo

Implementar la funcionalidad de **generación de descripción técnica** usando un modelo de lenguaje base (causal).
