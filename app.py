from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json
import re

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
    
    # Create employers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            website TEXT,
            verified INTEGER DEFAULT 0,
            felony_friendly INTEGER DEFAULT 1,
            contact_name TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Create jobs table
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
            is_active INTEGER DEFAULT 1,
            status TEXT DEFAULT 'pending',
            employer_id INTEGER,
            FOREIGN KEY (employer_id) REFERENCES employers(id)
        )
    ''')
    
    # Migrations for existing tables
    cursor.execute("PRAGMA table_info(jobs)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'status' not in columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN status TEXT DEFAULT 'approved'")
        print("Added status column to jobs table")
    
    if 'employer_id' not in columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN employer_id INTEGER REFERENCES employers(id)")
        print("Added employer_id column to jobs table")
    
    if 'view_count' not in columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN view_count INTEGER DEFAULT 0")
        print("Added view_count column to jobs table")
    
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
            'pending_jobs': '/api/jobs?status=pending',
            'approved_jobs': '/api/jobs?status=approved',
            'felony_friendly_jobs': '/api/jobs?felony_friendly=true',
            'search': '/api/jobs?search=keyword',
            'filter_by_location': '/api/jobs?location=Austin',
            'single_job': '/api/jobs/{id}',
            'create_job': 'POST /api/jobs',
            'update_job': 'PUT /api/jobs/{id}',
            'delete_job': 'DELETE /api/jobs/{id}',
            'admin_pending_jobs': 'GET /api/admin/jobs/pending',
            'admin_approve_job': 'POST /api/admin/jobs/{id}/approve',
            'admin_reject_job': 'POST /api/admin/jobs/{id}/reject',
            'all_employers': '/api/employers',
            'verified_employers': '/api/employers?verified=true',
            'single_employer': '/api/employers/{id}',
            'create_employer': 'POST /api/employers',
            'update_employer': 'PUT /api/employers/{id}',
            'admin_verify_employer': 'POST /api/admin/employers/{id}/verify'
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
    status = request.args.get('status', 'approved')
    days_posted = request.args.get('days_posted')
    min_salary = request.args.get('min_salary')
    max_salary = request.args.get('max_salary')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Validation
    if days_posted:
        try:
            days_posted = int(days_posted)
            if days_posted < 0:
                return jsonify({'error': 'days_posted must be a positive integer'}), 400
        except ValueError:
            return jsonify({'error': 'days_posted must be a valid integer'}), 400
    
    if min_salary:
        try:
            min_salary = float(min_salary)
        except ValueError:
            return jsonify({'error': 'min_salary must be a valid number'}), 400
    
    if max_salary:
        try:
            max_salary = float(max_salary)
        except ValueError:
            return jsonify({'error': 'max_salary must be a valid number'}), 400
    
    query = 'SELECT * FROM jobs WHERE is_active = 1'
    params = []
    
    if status and status != 'all':
        query += ' AND status = ?'
        params.append(status)
    
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
    
    if days_posted:
        query += " AND created_at >= datetime('now', '-' || ? || ' days')"
        params.append(days_posted)
    
    valid_sort_fields = ['created_at', 'title', 'company', 'view_count']
    if sort_by in valid_sort_fields:
        order = 'DESC' if sort_order.lower() == 'desc' else 'ASC'
        query += f' ORDER BY {sort_by} {order}'
    else:
        query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    jobs = []
    for row in rows:
        job_data = {
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
            'created_at': row['created_at'],
            'status': row['status'],
            'view_count': row['view_count'] if 'view_count' in row.keys() else 0
        }
        
        # Filter by salary range if specified
        if (min_salary or max_salary) and row['salary']:
            # Remove commas from salary string before parsing (e.g., "$50,000" -> "$50000")
            salary_normalized = row['salary'].replace(',', '')
            # Extract numbers from salary string (e.g., "$15-18/hour" -> [15, 18])
            numbers = re.findall(r'\d+(?:\.\d+)?', salary_normalized)
            if numbers:
                # Convert to floats and determine min/max from the salary range
                salary_values = [float(n) for n in numbers]
                salary_min = min(salary_values)
                salary_max = max(salary_values)
                
                # Check if the salary range overlaps with the filter range
                # min_salary filter: job's max must be >= requested min
                if min_salary and salary_max < min_salary:
                    continue
                # max_salary filter: job's max must be <= requested max
                if max_salary and salary_max > max_salary:
                    continue
        elif (min_salary or max_salary) and not row['salary']:
            # Skip jobs without salary info if filtering by salary
            continue
        
        jobs.append(job_data)
    
    conn.close()
    return jsonify(jobs), 200

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM jobs WHERE id = ? AND is_active = 1', (job_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    
    # Increment view count
    cursor.execute('UPDATE jobs SET view_count = view_count + 1 WHERE id = ?', (job_id,))
    conn.commit()
    
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
        'created_at': row['created_at'],
        'status': row['status'],
        'view_count': (row['view_count'] if 'view_count' in row.keys() else 0) + 1
    }
    
    conn.close()
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
    
    # Validate employer_id if provided
    employer_id = data.get('employer_id')
    if employer_id:
        cursor.execute('SELECT id FROM employers WHERE id = ? AND is_active = 1', (employer_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Invalid employer_id: employer not found'}), 400
    
    cursor.execute('''
        INSERT INTO jobs (
            title, company, location, description, salary, job_type,
            felony_friendly, background_check_details, contact_email,
            contact_phone, application_url, employer_id, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        data.get('application_url'),
        employer_id,
        'pending'
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
    
    # Validate employer_id if provided
    if 'employer_id' in data and data['employer_id'] is not None:
        cursor.execute('SELECT id FROM employers WHERE id = ? AND is_active = 1', (data['employer_id'],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Invalid employer_id: employer not found'}), 400
    
    fields = []
    values = []
    
    allowed_fields = [
        'title', 'company', 'location', 'description', 'salary', 'job_type',
        'felony_friendly', 'background_check_details', 'contact_email',
        'contact_phone', 'application_url', 'employer_id', 'is_active', 'status'
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

@app.route('/api/admin/jobs/<int:job_id>/approve', methods=['POST'])
def approve_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE jobs SET status = ? WHERE id = ?', ('approved', job_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Job approved successfully', 'job_id': job_id}), 200

@app.route('/api/admin/jobs/<int:job_id>/reject', methods=['POST'])
def reject_job(job_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE jobs SET status = ? WHERE id = ?', ('rejected', job_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Job not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Job rejected successfully', 'job_id': job_id}), 200

@app.route('/api/admin/jobs/pending', methods=['GET'])
def get_pending_jobs():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM jobs WHERE status = ? AND is_active = 1 ORDER BY created_at DESC', ('pending',))
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
            'created_at': row['created_at'],
            'status': row['status'],
            'view_count': row['view_count'] if 'view_count' in row.keys() else 0
        })
    
    conn.close()
    return jsonify(jobs), 200

@app.route('/api/employers', methods=['GET'])
def get_employers():
    conn = get_db()
    cursor = conn.cursor()
    
    verified_only = request.args.get('verified')
    
    query = 'SELECT * FROM employers WHERE is_active = 1'
    params = []
    
    if verified_only and verified_only.lower() == 'true':
        query += ' AND verified = 1'
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    employers = []
    for row in rows:
        employers.append({
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'website': row['website'],
            'verified': bool(row['verified']),
            'felony_friendly': bool(row['felony_friendly']),
            'contact_name': row['contact_name'],
            'contact_email': row['contact_email'],
            'contact_phone': row['contact_phone'],
            'created_at': row['created_at']
        })
    
    conn.close()
    return jsonify(employers), 200

@app.route('/api/employers/<int:employer_id>', methods=['GET'])
def get_employer(employer_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM employers WHERE id = ? AND is_active = 1', (employer_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return jsonify({'error': 'Employer not found'}), 404
    
    employer = {
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'website': row['website'],
        'verified': bool(row['verified']),
        'felony_friendly': bool(row['felony_friendly']),
        'contact_name': row['contact_name'],
        'contact_email': row['contact_email'],
        'contact_phone': row['contact_phone'],
        'created_at': row['created_at']
    }
    
    return jsonify(employer), 200

@app.route('/api/employers', methods=['POST'])
def create_employer():
    data = request.get_json()
    
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employers (
                name, description, website, felony_friendly, contact_name,
                contact_email, contact_phone, verified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data.get('description'),
            data.get('website'),
            1 if data.get('felony_friendly', True) else 0,
            data.get('contact_name'),
            data.get('contact_email'),
            data.get('contact_phone'),
            0
        ))
        
        employer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': employer_id, 'message': 'Employer created successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Employer with this name already exists'}), 409

@app.route('/api/employers/<int:employer_id>', methods=['PUT'])
def update_employer(employer_id):
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM employers WHERE id = ?', (employer_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Employer not found'}), 404
    
    fields = []
    values = []
    
    allowed_fields = [
        'name', 'description', 'website', 'felony_friendly',
        'contact_name', 'contact_email', 'contact_phone', 'is_active'
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
    
    values.append(employer_id)
    query = f"UPDATE employers SET {', '.join(fields)} WHERE id = ?"
    
    try:
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({'message': 'Employer updated successfully'}), 200
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Employer name must be unique'}), 409

@app.route('/api/admin/employers/<int:employer_id>/verify', methods=['POST'])
def verify_employer(employer_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE employers SET verified = 1 WHERE id = ?', (employer_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Employer not found'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Employer verified successfully', 'employer_id': employer_id}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
