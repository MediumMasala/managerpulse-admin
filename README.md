# ManagerPulse Django Admin

A Django admin dashboard for managing ManagerPulse data (Companies, Managers, Jobs, etc.)

## Setup

### 1. Install Dependencies

```bash
cd ratemymanager-admin
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Database

Edit `.env` file with your Supabase database credentials:

```env
DATABASE_HOST=db.your-project-id.supabase.co
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=your-database-password
DATABASE_PORT=5432
DATABASE_SSLMODE=require
```

**To get Supabase credentials:**
1. Go to your Supabase project dashboard
2. Click "Project Settings" > "Database"
3. Copy the connection details

### 3. Run Migrations (for Django auth tables only)

```bash
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver 8000
```

### 6. Access Admin

Open http://localhost:8000/admin and login with your superuser credentials.

## Features

- **Companies**: View, add, edit, and bulk import companies via CSV
- **Managers**: Manage manager profiles with company relationships
- **Job Postings**: CRUD and import for job listings
- **Private Notes**: View (read-only, encrypted content)
- **Extracted Signals**: View AI-extracted sentiment and ratings
- **Public Aggregates**: View computed aggregates
- **Appeals**: Manage user appeals
- **Moderation Queue**: Review flagged content
- **Audit Logs**: View system activity (read-only)

## CSV Import

For Companies, Managers, and Job Postings, use the "Import" button to bulk upload CSV files.

### Company CSV Format:
```csv
name,domain,lat,lng,city,region,country,logo_url,industry,size
Google,google.com,12.9716,77.5946,Bangalore,Karnataka,India,https://...,Technology,10000+
```

### Manager CSV Format:
```csv
company,display_name,title,team,location_text,is_verified
company_id_here,John Doe,Engineering Manager,Platform,Bangalore,false
```

### Job Posting CSV Format:
```csv
company,title,team,location_text,is_remote,source,url
company_id_here,Software Engineer,Engineering,Bangalore,true,manual,https://...
```

## Notes

- This Django admin connects to the same database as your Next.js app
- Models use `managed = False` so Django won't modify existing tables
- Encrypted data (notes) cannot be decrypted from the admin panel
- Audit logs are read-only for security
