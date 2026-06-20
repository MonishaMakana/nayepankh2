# Nayepankh Foundation - Volunteer Registration System

A comprehensive Django-based Volunteer Registration System for managing volunteers, tracking their contributions, and generating reports.

## Features

### 1. **Volunteer Registration**
- Easy registration with personal information
- Skills and availability selection
- Email verification system
- Profile management

### 2. **Authentication System**
- Secure login for volunteers
- Admin authentication with special permissions
- Session-based authentication
- Role-based access control (Volunteer vs Admin)

### 3. **Admin Dashboard**
- Dashboard with key statistics
- Pending volunteer approvals
- Active volunteer tracking
- Quick access to all management functions

### 4. **Volunteer Management**
- View all registered volunteers
- Filter by status, skills, or search by name/email
- Approve or reject volunteer applications
- Update volunteer hours contributed
- Track volunteer activity logs

### 5. **Reports Generation**
- Volunteer statistics (total, active, pending, inactive)
- Skills distribution analysis
- Top volunteers ranking
- Hours contributed tracking
- Export data as CSV or JSON

### 6. **Database**
- SQLite database for easy setup
- Comprehensive models for volunteers, admins, and activity logs
- Automatic timestamp tracking

## Project Structure

```
nayepankh-volunteer-system/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database
├── seed_data.py                 # Sample data script
├── README.md                    # This file
├── volunteer_system/            # Main project settings
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── volunteers/                  # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── forms.py                # Form definitions
│   ├── urls.py                 # App URL patterns
│   ├── admin.py                # Django admin customization
│   └── migrations/             # Database migrations
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── home.html               # Homepage
│   ├── register.html           # Volunteer registration
│   ├── login.html              # Volunteer login
│   ├── admin_login.html        # Admin login
│   ├── admin_dashboard.html    # Admin dashboard
│   ├── volunteer_list_admin.html # Volunteer management
│   ├── volunteer_profile.html  # Volunteer profile
│   ├── volunteer_edit.html     # Edit profile
│   ├── update_hours.html       # Update volunteer hours
│   ├── reports.html            # Reports and statistics
│   ├── about.html              # About page
│   └── contact.html            # Contact page
└── venv/                        # Virtual environment
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd nayepankh-volunteer-system
```

### Step 2: Create Virtual Environment (if not already done)
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations (if database doesn't exist)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin User (if needed)
```bash
python manage.py createsuperuser
```

Or use the demo credentials:
- Username: admin
- Password: admin@123

### Step 6: Load Sample Data (Optional)
```bash
python seed_data.py
```

This creates sample volunteers and demonstrates all features.

## Running the Application

### Start the Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

### Access Different Sections

1. **Homepage**: http://localhost:8000/
2. **Volunteer Registration**: http://localhost:8000/register/
3. **Volunteer Login**: http://localhost:8000/login/
4. **Admin Login**: http://localhost:8000/admin/login/
5. **Django Admin**: http://localhost:8000/admin/

## Demo Credentials

### Admin Account
- **Username**: admin
- **Password**: admin@123

### Sample Volunteer Accounts
After running `seed_data.py`, use any of these:
- **Email**: raj@example.com | **Password**: volunteer@123
- **Email**: priya@example.com | **Password**: volunteer@123
- **Email**: amit@example.com | **Password**: volunteer@123
- **Email**: neha@example.com | **Password**: volunteer@123
- **Email**: vikram@example.com | **Password**: volunteer@123
- **Email**: anjali@example.com | **Password**: volunteer@123

## Key Features & Workflows

### For Volunteers

1. **Registration**
   - Visit /register/ and fill in the form
   - Create a password-protected account
   - Application is automatically created with "Pending" status

2. **View Profile**
   - Login with your credentials
   - View your profile with all details
   - See your total hours contributed

3. **Edit Profile**
   - Update personal information
   - Change skills or availability
   - Update bio

4. **Track Hours**
   - Admins update your volunteer hours
   - See cumulative hours in your profile

### For Admins

1. **Dashboard**
   - View all key statistics at a glance
   - See pending approvals
   - Quick access to management features

2. **Manage Volunteers**
   - View all registered volunteers
   - Filter by status, skills, or search
   - Approve/reject pending applications
   - Update volunteer hours

3. **Generate Reports**
   - View comprehensive statistics
   - Analyze skills distribution
   - Identify top volunteers
   - Export data (CSV/JSON)

4. **Django Admin Interface**
   - Full database access and management
   - Customize admin settings
   - Manage activity logs

## Database Models

### Volunteer
- name, email, phone, address
- skills, availability, bio
- status (pending/active/inactive/rejected)
- hours_contributed, registration_date
- email_verified, verification_token

### ActivityLog
- volunteer (FK to Volunteer)
- activity_type (registration/approval/rejection/hours_update/etc)
- description, created_at, admin_user

### Report
- title, description, report_type
- data (JSON), generated_date

## API Endpoints (for reference)

### Public
- GET `/` - Homepage
- GET `/about/` - About page
- GET `/contact/` - Contact page
- GET/POST `/register/` - Volunteer registration
- GET/POST `/login/` - Volunteer login
- GET `/logout/` - Logout

### Volunteer (Requires Login)
- GET `/volunteer/<id>/` - View profile
- GET/POST `/volunteer/<id>/edit/` - Edit profile

### Admin (Requires Admin Login)
- GET `/admin/dashboard/` - Admin dashboard
- GET `/admin/volunteers/` - Volunteer management
- POST `/admin/volunteer/<id>/approve/` - Approve volunteer
- GET/POST `/admin/volunteer/<id>/hours/` - Update hours
- GET `/admin/reports/` - View reports
- GET `/admin/export/csv/` - Export as CSV
- GET `/admin/export/json/` - Export as JSON

## Customization

### Changing Email Settings
Edit `volunteer_system/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # For production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Modifying Skills or Availability Options
Edit `volunteers/models.py`:
```python
SKILLS_CHOICES = [
    ('new_skill', 'New Skill Name'),
    ...
]
```

### Customizing Styling
Edit `templates/base.html` in the `<style>` section, or modify Bootstrap variables.

## Troubleshooting

### 1. Database Errors
```bash
python manage.py flush  # Clear database
python manage.py migrate  # Re-create tables
python seed_data.py  # Re-populate sample data
```

### 2. Static Files Not Loading
```bash
python manage.py collectstatic
```

### 3. Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### 4. Database Locked
- Delete `db.sqlite3`
- Run migrations again
- Restart server

## Security Notes

⚠️ **For Production Use:**
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Use environment variables for sensitive data
- Set up proper email backend
- Use HTTPS
- Configure ALLOWED_HOSTS
- Use a production database (PostgreSQL/MySQL)

## Performance Tips

1. Use pagination for large volunteer lists
2. Enable database query caching
3. Optimize images and assets
4. Use CDN for static files
5. Set up proper logging and monitoring

## Support & Maintenance

- Regular database backups
- Monitor activity logs
- Update dependencies regularly
- Review security settings quarterly

## License

Nayepankh Foundation Volunteer System © 2024

## Contact

For support or inquiries:
- Email: info@nayepankh.org
- Website: www.nayepankh.org

---

**Happy Volunteering! 🤝**
