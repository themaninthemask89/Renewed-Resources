from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

DATABASE = 'jobs.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            salary TEXT,
            job_type TEXT,
            felony_friendly INTEGER NOT NULL DEFAULT 0,
            background_check_details TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            application_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Felony-Friendly Job Board API',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'all_jobs': '/api/jobs',
            'felony_friendly_jobs': '/api/jobs?felony_friendly=true',
            'search': '/api/jobs?search=keyword',
            'filter_by_location': '/api/jobs?location=Austin',
            'single_job': '/api/jobs/{id}',
            'create_job': 'POST /api/jobs',
            'update_job': 'PUT /api/jobs/{id}',
            'delete_job': 'DELETE /api/jobs/{id}'
        },
        'documentation': 'See API_DOCUMENTATION.md for full details'
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = get_db()
    cursor = conn.cursor()
    
    felony_friendly = request.args.get('felony_friendly')
    location = request.args.get('location')
    job_type = request.args.get('job_type')
    search = request.args.get('search')
    
    query = 'SELECT * FROM jobs WHERE is_active = 1'
    params = []
    
    if felony_friendly:
        query += ' AND felony_friendly = ?'
        params.append(1 if felony_friendly.lower() == 'true' else 0)
    
    if location:
        query += ' AND location LIKE ?'
        params.append(f'%{location}%')
    
    if job_type:
        query += ' AND job_type = ?'
        params.append(job_type)
    
    if search:
        query += ' AND (title LIKE ? OR company LIKE ? OR description LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    jobs = []
    for row in rows:
        jobs.append({
            'id': row['id'],
            'title': row['title'],
            'company': row['company'],
            'location': row['location'],
            'description': row['description'],
            'salary': row['salary'],
            'job_type': row['job_type'],
            'felony_friendly': bool(row['felony_friendly']),
            'background_check_details': row['background_check_details'],
            'contact_email': row['contact_email'],
            'contact_phone': row['contact_phone'],
            'application_url': row['application_url'],
            'created_at': row['created_at']
        })
    
    conn.close()
    return jsonify(jobs), 200

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM jobs WHERE id = ? AND is_active = 1', (job_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return jsonify({'error': 'Job not found'}), 404
    
    job = {
        'id': row['id'],
        'title': row['title'],
        'company': row['company'],
        'location': row['location'],
        'description': row['description'],
        'salary': row['salary'],
        'job_type': row['job_type'],
        'felony_friendly': bool(row['felony_friendly']),
        'background_check_details': row['background_check_details'],
        'contact_email': row['contact_email'],
        'contact_phone': row['contact_phone'],
        'application_url': row['application_url'],
        'created_at': row['created_at']
    }
    
    return jsonify(job), 200

@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    
    required_fields = ['title', 'company', 'location', 'description']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO jobs (
            title, company, location, description, salary, job_type,
            felony_friendly, background_check_details, contact_email,
            contact_phone, application_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['title'],
        data['company'],
        data['location'],
        data['description'],
        data.get('salary'),
        data.get('job_type'),
        1 if data.get('felony_friendly') else 0,
        data.get('background_check_details'),
        data.get('contact_email'),
        data.get('contact_phone'),
        data.get('application_url')
    ))
    
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': job_id, 'message': 'Job created successfully'}), 201

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM jobs WHERE id = ?', (job_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    
    fields = []
    values = []
    
    allowed_fields = [
        'title', 'company', 'location', 'description', 'salary', 'job_type',
        'felony_friendly', 'background_check_details', 'contact_email',
        'contact_phone', 'application_url', 'is_active'
    ]
    
    for field in allowed_fields:
        if field in data:
            if field == 'felony_friendly':
                fields.append(f'{field} = ?')
                values.append(1 if data[field] else 0)
            else:
                fields.append(f'{field} = ?')
                values.append(data[field])
    
    if not fields:
        conn.close()
        return jsonify({'error': 'No valid fields to update'}), 400
    
    values.append(job_id)
    query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = ?"
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Job updated successfully'}), 200

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE jobs SET is_active = 0 WHERE id = ?', (job_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Job deleted successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
