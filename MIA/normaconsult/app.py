from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import re

app = Flask(__name__)

# Rutas de datos
TICKETS_FILE = 'data/tickets.json'
NORMATIVAS_DIR = 'data/normativas'

# Cargar tickets
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tickets(tickets):
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# ============= SISTEMA DE TICKETS =============

@app.route('/tickets')
def tickets_page():
    return render_template('tickets.html')

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    tickets = load_tickets()
    status = request.args.get('status', 'all')
    
    if status != 'all':
        tickets = [t for t in tickets if t['status'] == status]
    
    return jsonify(tickets)

@app.route('/api/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    
    if ticket:
        return jsonify(ticket)
    return jsonify({'error': 'Ticket no encontrado'}), 404

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    tickets = load_tickets()
    data = request.json
    
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = data.get('status', ticket['status'])
            ticket['respuesta'] = data.get('respuesta', ticket['respuesta'])
            ticket['fecha_respuesta'] = datetime.now().isoformat()
            save_tickets(tickets)
            return jsonify(ticket)
    
    return jsonify({'error': 'Ticket no encontrado'}), 404

# ============= BÚSQUEDA DE NORMATIVAS =============

@app.route('/normativas')
def normativas_page():
    return render_template('normativas.html')

@app.route('/api/normativas/list', methods=['GET'])
def list_normativas():
    """Lista todos los documentos disponibles"""
    normativas = []
    
    if os.path.exists(NORMATIVAS_DIR):
        for filename in os.listdir(NORMATIVAS_DIR):
            if filename.endswith('.txt'):
                filepath = os.path.join(NORMATIVAS_DIR, filename)
                normativas.append({
                    'nombre': filename.replace('.txt', ''),
                    'archivo': filename
                })
    
    return jsonify(normativas)

@app.route('/api/normativas/search', methods=['POST'])
def search_normativas():
    """Búsqueda por palabra clave simple (keyword matching)"""
    data = request.json
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({'results': []})
    
    results = []
    
    if os.path.exists(NORMATIVAS_DIR):
        for filename in os.listdir(NORMATIVAS_DIR):
            if filename.endswith('.txt'):
                filepath = os.path.join(NORMATIVAS_DIR, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Búsqueda simple por palabra clave
                lines = content.split('\n')
                matches = []
                
                for i, line in enumerate(lines):
                    if query in line.lower():
                        # Contexto: línea anterior, actual y siguiente
                        start = max(0, i-1)
                        end = min(len(lines), i+2)
                        context = '\n'.join(lines[start:end])
                        
                        matches.append({
                            'line_number': i + 1,
                            'context': context,
                            'line': line
                        })
                
                if matches:
                    results.append({
                        'documento': filename.replace('.txt', ''),
                        'archivo': filename,
                        'num_coincidencias': len(matches),
                        'coincidencias': matches[:5]  # Primeras 5
                    })
    
    return jsonify({'results': results, 'query': query})

@app.route('/api/normativas/download/<filename>')
def download_normativa(filename):
    """Descargar documento completo"""
    filepath = os.path.join(NORMATIVAS_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'Archivo no encontrado'}), 404

if __name__ == '__main__':
    # Crear directorios si no existen
    os.makedirs('data', exist_ok=True)
    os.makedirs(NORMATIVAS_DIR, exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5011)
