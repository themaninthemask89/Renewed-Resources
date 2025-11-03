# Felony-Friendly Job Board - Backend API

## Project Overview
This is a REST API backend for a job board specifically designed to help people with felonies and criminal backgrounds find employment. The API focuses on curating and displaying jobs from employers who are explicitly open to hiring individuals with criminal records.

## Current Status
**Backend API is fully functional** with all core endpoints working:
- Job listing retrieval with filtering
- Job creation, updating, and deletion
- Search functionality
- Felony-friendly filtering

## Recent Changes (November 2, 2025)
- Created Python Flask REST API with complete CRUD operations
- Set up SQLite database with jobs schema
- Implemented filtering by location, job type, and felony-friendly status
- Added search functionality across title, company, and description
- Seeded database with 5 sample felony-friendly job listings
- Created comprehensive API documentation
- Configured Flask server to run on port 5000

## User Preferences & Goals
- **Development Approach**: Functionality first, UI later ("inside out" approach)
- **Strategy**: Quality over quantity - curate verified felony-friendly employers rather than scraping millions of generic jobs
- **Architecture**: Backend API + separate frontend (user plans to use external UI builder like Bubble.io, Webflow, or similar)
- **Key Differentiator**: Every job on the board is verified as accessible to people with criminal backgrounds

## Project Architecture

### Tech Stack
- **Backend**: Python 3.11 + Flask
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **API Format**: REST with JSON responses
- **CORS**: Enabled for cross-origin requests

### File Structure
```
.
├── app.py                    # Main Flask application with all API endpoints
├── seed_data.py             # Script to populate database with sample jobs
├── jobs.db                  # SQLite database (auto-generated)
├── API_DOCUMENTATION.md     # Complete API documentation
└── replit.md               # This file
```

### Database Schema
**Jobs Table:**
- `id`: Primary key
- `title`, `company`, `location`, `description`: Required fields
- `salary`, `job_type`: Optional job details
- `felony_friendly`: Boolean flag (critical field)
- `background_check_details`: Transparency about hiring practices
- `contact_email`, `contact_phone`, `application_url`: Contact information
- `created_at`: Timestamp
- `is_active`: For soft deletes

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/jobs` | Get all jobs (with optional filters) |
| GET | `/api/jobs/{id}` | Get single job details |
| POST | `/api/jobs` | Create new job |
| PUT | `/api/jobs/{id}` | Update job |
| DELETE | `/api/jobs/{id}` | Soft-delete job |

**Supported Filters:**
- `?felony_friendly=true` - Show only felony-friendly jobs
- `?location=Austin` - Filter by location
- `?job_type=Full-time` - Filter by job type
- `?search=warehouse` - Search across title/company/description

## Key Features Implemented
✅ Complete CRUD operations for jobs  
✅ Filtering and search functionality  
✅ Felony-friendly job flagging  
✅ Background check transparency field  
✅ Soft deletes (jobs marked inactive, not removed)  
✅ Sample data with 5 verified felony-friendly jobs  
✅ CORS enabled for any frontend  
✅ Full API documentation  

## Next Steps (Not Yet Implemented)
- User authentication (job seekers & employers)
- Email notifications
- Admin panel for job approval
- Integration with job scraping services (only for verified felony-friendly employers)
- PostgreSQL upgrade for production
- Employer verification system
- Partnership with reentry programs

## How to Use

### Running the API
The Flask server runs automatically via the configured workflow:
```bash
python app.py
```
Server runs on `http://0.0.0.0:5000`

### Adding Sample Data
```bash
python seed_data.py
```

### Testing Endpoints
```bash
# Get all jobs
curl http://localhost:5000/api/jobs

# Get felony-friendly jobs only
curl "http://localhost:5000/api/jobs?felony_friendly=true"

# Search for jobs
curl "http://localhost:5000/api/jobs?search=warehouse"

# Create a job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Driver","company":"ABC Transport","location":"Dallas, TX","description":"Delivery driver position","felony_friendly":true}'
```

## Connecting Frontend Builders
This API is designed to work with:
- **Bubble.io** (via API Connector)
- **Webflow** (via custom code or Wized)
- **Retool** (REST API resource)
- **Softr** (external API connection)
- **Custom React/Vue/Angular apps**

See `API_DOCUMENTATION.md` for integration examples.

## Important Notes
- The code is fully portable - not locked into Replit
- Uses standard REST conventions
- Can be deployed anywhere (Heroku, Vercel, AWS, etc.)
- Database can be easily switched to PostgreSQL
- All responses are in JSON format for universal compatibility

## Project Philosophy
The value proposition is **curation and trust**, not volume. Job seekers with criminal backgrounds need to know that every job listing is genuinely accessible to them, rather than applying to hundreds of jobs that will automatically reject them. This API is built to support that mission by focusing on verified felony-friendly employers.
