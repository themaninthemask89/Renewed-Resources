import sqlite3

DATABASE = 'jobs.db'

def seed_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    sample_jobs = [
        {
            'title': 'Warehouse Associate',
            'company': 'Second Chance Logistics',
            'location': 'Dallas, TX',
            'description': 'We are actively hiring individuals with criminal backgrounds. Full-time warehouse position with benefits. Responsibilities include loading, unloading, inventory management.',
            'salary': '$15-18/hour',
            'job_type': 'Full-time',
            'felony_friendly': 1,
            'background_check_details': 'We conduct background checks but consider all applicants regardless of criminal history',
            'contact_email': 'jobs@secondchancelogistics.com',
            'application_url': 'https://example.com/apply'
        },
        {
            'title': 'Kitchen Staff',
            'company': 'Fresh Start Cafe',
            'location': 'Austin, TX',
            'description': 'Entry-level kitchen position. We believe in second chances and actively recruit from reentry programs. Training provided.',
            'salary': '$14/hour + tips',
            'job_type': 'Full-time',
            'felony_friendly': 1,
            'background_check_details': 'No background check required',
            'contact_email': 'hiring@freshstartcafe.com',
            'contact_phone': '512-555-0123',
            'application_url': 'https://example.com/apply'
        },
        {
            'title': 'Construction Laborer',
            'company': 'Rebuild Construction Co.',
            'location': 'Houston, TX',
            'description': 'Construction laborer needed. Felony-friendly employer. Must be willing to work outdoors and lift 50lbs. PPE provided.',
            'salary': '$16-20/hour based on experience',
            'job_type': 'Full-time',
            'felony_friendly': 1,
            'background_check_details': 'Background check conducted but felonies are not automatically disqualifying',
            'contact_email': 'careers@rebuildconstruction.com',
            'contact_phone': '713-555-0199',
            'application_url': 'https://example.com/apply'
        },
        {
            'title': 'Delivery Driver',
            'company': 'Fair Chance Transport',
            'location': 'San Antonio, TX',
            'description': 'Local delivery routes. Valid drivers license required. We partner with reentry programs and welcome applications from those with criminal records.',
            'salary': '$17/hour + mileage',
            'job_type': 'Full-time',
            'felony_friendly': 1,
            'background_check_details': 'Driving record check required, criminal background considered on case-by-case basis',
            'contact_email': 'drivers@fairchancetransport.com',
            'application_url': 'https://example.com/apply'
        },
        {
            'title': 'Manufacturing Operator',
            'company': 'New Horizons Manufacturing',
            'location': 'Fort Worth, TX',
            'description': 'Operating machinery in climate-controlled facility. No experience necessary, full training provided. Benefits after 90 days.',
            'salary': '$16.50/hour',
            'job_type': 'Full-time',
            'felony_friendly': 1,
            'background_check_details': 'We are a Ban the Box employer and consider all applicants fairly',
            'contact_email': 'hr@newhorizonsmfg.com',
            'contact_phone': '817-555-0156',
            'application_url': 'https://example.com/apply'
        }
    ]
    
    for job in sample_jobs:
        cursor.execute('''
            INSERT INTO jobs (
                title, company, location, description, salary, job_type,
                felony_friendly, background_check_details, contact_email,
                contact_phone, application_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job['title'],
            job['company'],
            job['location'],
            job['description'],
            job['salary'],
            job['job_type'],
            job['felony_friendly'],
            job['background_check_details'],
            job.get('contact_email'),
            job.get('contact_phone'),
            job.get('application_url')
        ))
    
    conn.commit()
    conn.close()
    print(f"Seeded {len(sample_jobs)} sample jobs into the database")

if __name__ == '__main__':
    seed_database()
