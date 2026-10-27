# 🏗️ NormaConsult - Sistema de Gestión de Consultas Técnicas

## 📋 Descripción

Sistema base para el **Reto NormaConsult**. Este sistema permite gestionar tickets de consultas técnicas y buscar información en documentos normativos de construcción.

## 🚀 Instalación y Despliegue

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Descomprimir el archivo

```bash
unzip normaconsult.zip -d normaconsult
cd normaconsult
```

### Paso 2: Crear entorno virtual (recomendado)

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5010**

## 📂 Estructura del Proyecto

```
normaconsult/
│
├── app.py                          # Aplicación Flask principal
├── requirements.txt                # Dependencias Python
├── README.md                       # Este archivo
│
├── templates/                      # Plantillas HTML
│   ├── index.html                 # Página principal
│   ├── tickets.html               # Sistema de tickets
│   └── normativas.html            # Búsqueda de normativas
│
└── data/                           # Datos de la aplicación
    ├── tickets.json               # Base de datos de tickets (15 tickets sintéticos)
    └── normativas/                # Documentos normativos
        ├── CTE_DB-HE_Eficiencia_Energetica.txt
        ├── CTE_DB-SI_Seguridad_Incendios.txt
        ├── CTE_DB-HS_Salubridad.txt
        └── CTE_DB-SUA_Accesibilidad.txt
```

## 🎮 Uso de la Aplicación

### 1. Sistema de Tickets

- Accede desde la página principal o directamente en `/tickets`
- Visualiza tickets pendientes, en proceso y resueltos
- Haz clic en un ticket para ver detalles y responder
- Guarda respuestas que se almacenan automáticamente

**Funcionalidad actual:**
- CRUD simple de tickets
- Filtrado por estado
- Sin inteligencia artificial

### 2. Base de Conocimiento (Normativas)

- Accede desde la página principal o directamente en `/normativas`
- Busca por palabras clave en los documentos
- Descarga documentos completos
- Visualiza coincidencias con contexto

**Funcionalidad actual:**
- Búsqueda por palabra clave exacta (case-insensitive)
- Muestra contexto alrededor de las coincidencias
- No hay búsqueda semántica ni vectorial

## 📊 Datos Incluidos

### Tickets (15 ejemplos)

- 6 tickets resueltos (con respuesta)
- 2 tickets en proceso
- 7 tickets pendientes

Los tickets cubren consultas típicas sobre:
- Aislamiento térmico
- Resistencia al fuego
- Ventilación y salubridad
- Accesibilidad
- Certificación energética
- Instalaciones contra incendios

### Documentos Normativos (4 documentos)

> **Importante:** son versiones **simplificadas y ficticias** de cuatro documentos básicos del CTE, creadas para el reto. Algunos valores no coinciden con el Código Técnico de la Edificación real, así que no los uses como referencia profesional. El texto oficial está en [codigotecnico.org](https://www.codigotecnico.org).

1. **CTE DB-HE** - Eficiencia Energética (~120 líneas)
   - Transmitancia térmica
   - Zonas climáticas
   - Aislamiento
   - Certificación energética

2. **CTE DB-SI** - Seguridad Contra Incendios (~200 líneas)
   - Resistencia al fuego
   - Columna seca
   - Extintores y BIEs
   - Evacuación

3. **CTE DB-HS** - Salubridad (~230 líneas)
   - Ventilación
   - Suministro de agua
   - Evacuación de aguas
   - Calidad del aire interior

4. **CTE DB-SUA** - Accesibilidad (~260 líneas)
   - Rampas y escaleras
   - Itinerarios accesibles
   - Aseos adaptados
   - Plazas de aparcamiento PMR

## 📝 Notas Técnicas

### Base de Datos

Los tickets se almacenan en `data/tickets.json`. Es un archivo JSON simple que se lee/escribe con cada operación. Para un sistema real se recomienda usar una base de datos relacional (PostgreSQL, MySQL) o NoSQL (MongoDB).

### Búsqueda Actual

La búsqueda de normativas es muy básica:
- Lee cada archivo línea por línea
- Busca la palabra clave con `.lower()`
- Devuelve contexto (línea anterior, actual, siguiente)

### Escalabilidad

Este sistema NO está diseñado para producción:
- Sin autenticación
- Sin validación robusta
- Sin logging
- Sin pruebas
- Sin caché

## 🐛 Solución de Problemas

### Error: "Address already in use"

El puerto 5010 está ocupado. Cambia el puerto en la última línea de `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5011)
```

### Error: "Module not found"

Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Los archivos no se guardan

Verifica permisos de escritura en la carpeta `data/`:
```bash
chmod -R 755 data/
```

### PROBLEMATICA

El sistema funciona, pero es poco eficiente. El personal tarda una media de 2 horas en responder cada ticket y está bastante frustrado. Cuando se le pregunta qué ocurre, comenta dos problemas:

- El buscador solo encuentra palabras exactas. Si buscan "aislamiento de fachada", no aparece nada, aunque el documento de ahorro de energía tiene un apartado entero sobre la "transmitancia térmica" de los "muros de fachada". Si buscan "escalera de emergencia", tampoco, porque el documento habla de "escaleras" en el apartado de "evacuación de ocupantes". Así que van probando palabras hasta dar con algo, o leen los documentos enteros. "Buscar es más difícil que responder", dice uno de ellos.
- Responden una y otra vez consultas parecidas. Muchas consultas se parecen a otras que ya se respondieron, pero no hay forma de encontrarlas. "Estoy seguro de que esto ya lo respondí hace un mes, pero no encuentro dónde" es una frase que se oye constantemente. Al final, escriben la misma respuesta desde cero.
  
La dirección quiere bajar el tiempo de respuesta a menos de 1 hora por ticket.

¿Puedes modificar la aplicación para que el personal encuentre la información más rápido y pueda reutilizar las respuestas anteriores?

### Solución

Usar una RAG, y que la IA analice las respuestas ya dadas, y que lea toda la base de conocimiento