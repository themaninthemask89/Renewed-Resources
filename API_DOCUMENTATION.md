# Felony-Friendly Job Board API Documentation

## Overview
This is a REST API for managing job listings specifically for people with criminal backgrounds. The API returns JSON data and can be connected to any frontend (Bubble.io, Webflow, custom React app, etc.).

## Base URL
When running locally: `http://localhost:5000`
When deployed on Replit: Your Replit deployment URL

## Endpoints

### Health Check
**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

### Get All Jobs
**GET** `/api/jobs`

Retrieve all active job listings with optional filters. **By default, only returns approved jobs** unless `status` parameter is specified.

**Query Parameters:**
- `felony_friendly` (optional): Filter for felony-friendly jobs. Set to `true` to show only felony-friendly jobs.
- `location` (optional): Filter jobs by location. Partial matching supported (e.g., "Austin" will match "Austin, TX").
- `job_type` (optional): Filter by job type (e.g., "Full-time", "Part-time").
- `search` (optional): Search across job title, company name, and description.
- `status` (optional): Filter by approval status ("pending", "approved", "rejected"). Defaults to "approved".
- `min_salary` (optional): Minimum salary filter (numeric value, e.g., 15 for $15/hour or 50000 for $50k/year).
- `max_salary` (optional): Maximum salary filter (numeric value).
- `days_posted` (optional): Show jobs posted within the last N days (e.g., 7 for last week, 30 for last month).
- `sort_by` (optional): Sort results by field ("created_at", "title", "company", "view_count"). Default: "created_at".
- `sort_order` (optional): Sort direction ("asc" or "desc"). Default: "desc".

**Examples:**
```bash
# Get all approved jobs (default)
GET /api/jobs

# Get only felony-friendly jobs
GET /api/jobs?felony_friendly=true

# Get jobs in Austin
GET /api/jobs?location=Austin

# Search for "warehouse" jobs
GET /api/jobs?search=warehouse

# Get jobs with salary $16/hour or higher
GET /api/jobs?min_salary=16

# Get jobs with salary between $50k-70k/year
GET /api/jobs?min_salary=50000&max_salary=70000

# Get jobs posted in the last 7 days
GET /api/jobs?days_posted=7

# Get pending jobs (admin use)
GET /api/jobs?status=pending

# Sort by most viewed jobs
GET /api/jobs?sort_by=view_count&sort_order=desc

# Combine filters: felony-friendly jobs in Dallas with $15+ salary
GET /api/jobs?felony_friendly=true&location=Dallas&min_salary=15
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Warehouse Associate",
    "company": "Second Chance Logistics",
    "location": "Dallas, TX",
    "description": "We are actively hiring individuals with criminal backgrounds...",
    "salary": "$15-18/hour",
    "job_type": "Full-time",
    "felony_friendly": true,
    "background_check_details": "We conduct background checks but consider all applicants...",
    "contact_email": "jobs@secondchancelogistics.com",
    "contact_phone": null,
    "application_url": "https://example.com/apply",
    "created_at": "2025-11-02 15:41:39",
    "status": "approved",
    "view_count": 42
  }
]
```

---

### Get Single Job
**GET** `/api/jobs/{job_id}`

Retrieve details for a specific job. **Automatically increments the view_count for analytics tracking.**

**Example:**
```bash
GET /api/jobs/1
```

**Response:**
```json
{
  "id": 1,
  "title": "Warehouse Associate",
  "company": "Second Chance Logistics",
  "location": "Dallas, TX",
  "description": "We are actively hiring individuals with criminal backgrounds...",
  "salary": "$15-18/hour",
  "job_type": "Full-time",
  "felony_friendly": true,
  "background_check_details": "We conduct background checks but consider all applicants...",
  "contact_email": "jobs@secondchancelogistics.com",
  "contact_phone": null,
  "application_url": "https://example.com/apply",
  "created_at": "2025-11-02 15:41:39",
  "status": "approved",
  "view_count": 43
}
```

**Error Response (404):**
```json
{
  "error": "Job not found"
}
```

---

### Create New Job
**POST** `/api/jobs`

Create a new job listing. **Jobs are created with "pending" status by default** and require admin approval.

**Required Fields:**
- `title` (string): Job title
- `company` (string): Company name
- `location` (string): Job location
- `description` (string): Job description

**Optional Fields:**
- `salary` (string): Salary information
- `job_type` (string): Job type (e.g., "Full-time", "Part-time", "Contract")
- `felony_friendly` (boolean): Whether the employer is felony-friendly
- `background_check_details` (string): Information about background checks
- `contact_email` (string): Contact email
- `contact_phone` (string): Contact phone number
- `application_url` (string): URL to apply
- `employer_id` (integer): Link to verified employer profile

**Example Request:**
```bash
POST /api/jobs
Content-Type: application/json

{
  "title": "Truck Driver",
  "company": "Open Road Transport",
  "location": "El Paso, TX",
  "description": "CDL truck driver position. We hire individuals with criminal backgrounds.",
  "salary": "$50,000-65,000/year",
  "job_type": "Full-time",
  "felony_friendly": true,
  "background_check_details": "Background check required but not disqualifying",
  "contact_email": "hiring@openroadtransport.com"
}
```

**Success Response (201):**
```json
{
  "id": 6,
  "message": "Job created successfully"
}
```

**Error Response (400):**
```json
{
  "error": "Missing required field: title"
}
```

---

### Update Job
**PUT** `/api/jobs/{job_id}`

Update an existing job listing.

**Example Request:**
```bash
PUT /api/jobs/1
Content-Type: application/json

{
  "salary": "$16-20/hour",
  "description": "Updated job description..."
}
```

**Success Response (200):**
```json
{
  "message": "Job updated successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Job not found"
}
```

---

### Delete Job
**DELETE** `/api/jobs/{job_id}`

Soft-delete a job (marks it as inactive rather than removing it from database).

**Example:**
```bash
DELETE /api/jobs/1
```

**Success Response (200):**
```json
{
  "message": "Job deleted successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Job not found"
}
```

---

### Approve Job
**POST** `/api/admin/jobs/{job_id}/approve`

Approve a pending job listing (admin operation). Changes job status from "pending" to "approved".

**Example:**
```bash
POST /api/admin/jobs/1/approve
```

**Success Response (200):**
```json
{
  "message": "Job approved successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Job not found"
}
```

---

### Reject Job
**POST** `/api/admin/jobs/{job_id}/reject`

Reject a pending job listing (admin operation). Changes job status to "rejected".

**Example:**
```bash
POST /api/admin/jobs/1/reject
```

**Success Response (200):**
```json
{
  "message": "Job rejected successfully"
}
```

---

### Get All Employers
**GET** `/api/employers`

Retrieve all employer profiles with optional verification filter.

**Query Parameters:**
- `verified` (optional): Set to `true` to show only verified employers.

**Examples:**
```bash
# Get all employers
GET /api/employers

# Get only verified employers
GET /api/employers?verified=true
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Second Chance Logistics",
    "description": "We believe in second chances and actively hire individuals with criminal backgrounds.",
    "website": "https://secondchancelogistics.com",
    "verified": true,
    "felony_friendly": true,
    "contact_name": "Jane Smith",
    "contact_email": "jobs@secondchancelogistics.com",
    "contact_phone": "(555) 123-4567",
    "created_at": "2025-11-02 15:41:39"
  }
]
```

---

### Create Employer Profile
**POST** `/api/employers`

Create a new employer profile.

**Required Fields:**
- `name` (string): Company name

**Optional Fields:**
- `description` (string): Company description
- `website` (string): Company website URL
- `felony_friendly` (boolean): Whether employer is felony-friendly (defaults to true)
- `contact_name` (string): Contact person name
- `contact_email` (string): Contact email
- `contact_phone` (string): Contact phone number

**Example Request:**
```bash
POST /api/employers
Content-Type: application/json

{
  "name": "New Beginnings Construction",
  "description": "Construction company committed to hiring individuals with criminal backgrounds.",
  "felony_friendly": true,
  "contact_name": "John Doe",
  "contact_email": "hr@newbeginnings.com",
  "contact_phone": "(555) 987-6543",
  "website": "https://newbeginnings.com"
}
```

**Success Response (201):**
```json
{
  "id": 2,
  "message": "Employer created successfully"
}
```

**Error Response (400):**
```json
{
  "error": "Missing required field: company_name"
}
```

---

### Update Employer Profile
**PUT** `/api/employers/{employer_id}`

Update an existing employer profile.

**Example Request:**
```bash
PUT /api/employers/1
Content-Type: application/json

{
  "description": "Updated company description...",
  "contact_phone": "(555) 111-2222"
}
```

**Success Response (200):**
```json
{
  "message": "Employer updated successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Employer not found"
}
```

---

### Verify Employer
**POST** `/api/admin/employers/{employer_id}/verify`

Mark an employer as verified (admin operation). Sets `verified` to true.

**Example:**
```bash
POST /api/admin/employers/1/verify
```

**Success Response (200):**
```json
{
  "message": "Employer verified successfully"
}
```

**Error Response (404):**
```json
{
  "error": "Employer not found"
}
```

---

## Connecting to Frontend Builders

### Bubble.io
1. Use the API Connector plugin
2. Add a new API with base URL: `https://your-replit-url.replit.app`
3. Create calls for each endpoint
4. Use dynamic data to populate repeating groups

### Webflow
1. Use custom code or Wized/Xano integration
2. Make fetch requests to the API endpoints
3. Populate CMS or dynamic lists with the data

### Retool
1. Add a REST API resource
2. Point it to your Replit deployment URL
3. Create queries for each endpoint
4. Build UI components connected to the queries

### Custom Frontend (React, Vue, etc.)
```javascript
// Example: Fetch all felony-friendly jobs
fetch('https://your-api-url.replit.app/api/jobs?felony_friendly=true')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

## Database Schema

### Jobs Table
- `id`: Auto-incrementing primary key
- `title`: Job title (required)
- `company`: Company name (required)
- `location`: Job location (required)
- `description`: Job description (required)
- `salary`: Salary information
- `job_type`: Type of employment
- `felony_friendly`: Boolean (0 or 1)
- `background_check_details`: Information about background checks
- `contact_email`: Contact email
- `contact_phone`: Contact phone
- `application_url`: URL to apply
- `employer_id`: Foreign key to employers table (optional)
- `created_at`: Timestamp when job was created
- `is_active`: Boolean (0 or 1) for soft deletes
- `status`: Job approval status ("pending", "approved", "rejected")
- `view_count`: Number of times job was viewed (for analytics)

### Employers Table
- `id`: Auto-incrementing primary key
- `name`: Company name (required, unique)
- `description`: Company description
- `website`: Company website URL
- `verified`: Boolean (0 or 1) - whether employer is verified
- `felony_friendly`: Boolean (0 or 1) - whether employer is felony-friendly (defaults to 1)
- `contact_name`: Contact person name
- `contact_email`: Contact email
- `contact_phone`: Contact phone number
- `created_at`: Timestamp when employer profile was created
- `is_active`: Boolean (0 or 1) for soft deletes

---

## Notes

- The API uses SQLite database (stored in `jobs.db` file)
- To upgrade to PostgreSQL later, the code can be easily modified
- All jobs are soft-deleted (marked inactive) rather than permanently removed
- The database includes 5 sample felony-friendly jobs and 1 sample employer to get started
- CORS is enabled, so you can call this API from any frontend
- **Job approval workflow**: All new jobs default to "pending" status and require admin approval
- **Analytics tracking**: View counts are automatically incremented when jobs are viewed
- **Salary filtering**: Intelligently handles various salary formats including ranges and comma-separated numbers
- **Employer verification**: Employers can be verified by admins to build trust with job seekers

---

## Next Steps

1. Deploy this API on Replit to get a permanent URL
2. Connect your chosen frontend builder to the API (Bubble.io, Webflow, etc.)
3. Set up an admin interface for approving/rejecting jobs and verifying employers
4. Add real job listings from verified felony-friendly employers
5. Monitor popular jobs using the view_count analytics
6. Consider adding user authentication for job seekers and employers
7. Add email notifications when new jobs are approved
8. Build employer profiles to showcase verified felony-friendly companies
