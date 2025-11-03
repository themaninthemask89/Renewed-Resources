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

Retrieve all active job listings with optional filters.

**Query Parameters:**
- `felony_friendly` (optional): Filter for felony-friendly jobs. Set to `true` to show only felony-friendly jobs.
- `location` (optional): Filter jobs by location. Partial matching supported (e.g., "Austin" will match "Austin, TX").
- `job_type` (optional): Filter by job type (e.g., "Full-time", "Part-time").
- `search` (optional): Search across job title, company name, and description.

**Examples:**
```bash
# Get all jobs
GET /api/jobs

# Get only felony-friendly jobs
GET /api/jobs?felony_friendly=true

# Get jobs in Austin
GET /api/jobs?location=Austin

# Search for "warehouse" jobs
GET /api/jobs?search=warehouse

# Combine filters: felony-friendly jobs in Dallas
GET /api/jobs?felony_friendly=true&location=Dallas
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
    "created_at": "2025-11-02 15:41:39"
  }
]
```

---

### Get Single Job
**GET** `/api/jobs/{job_id}`

Retrieve details for a specific job.

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
  "created_at": "2025-11-02 15:41:39"
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

Create a new job listing.

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
- `created_at`: Timestamp when job was created
- `is_active`: Boolean (0 or 1) for soft deletes

---

## Notes

- The API uses SQLite database (stored in `jobs.db` file)
- To upgrade to PostgreSQL later, the code can be easily modified
- All jobs are soft-deleted (marked inactive) rather than permanently removed
- The database includes 5 sample felony-friendly jobs to get started
- CORS is enabled, so you can call this API from any frontend

---

## Next Steps

1. Deploy this API on Replit to get a permanent URL
2. Connect your chosen frontend builder to the API
3. Add real job listings from felony-friendly employers
4. Consider adding user authentication for job seekers and employers
5. Add email notifications when new jobs are posted
