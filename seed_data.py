import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volunteer_system.settings')
django.setup()

from django.contrib.auth.models import User
from volunteers.models import Volunteer, ActivityLog
from datetime import datetime, timedelta

# Create admin user
try:
    admin = User.objects.create_superuser('admin', 'admin@nayepankh.org', 'admin@123')
    admin.is_staff = True
    admin.save()
    print("[SUCCESS] Admin user created: admin / admin@123")
except Exception as e:
    print(f"[INFO] Admin user already exists or error: {e}")

# Create sample volunteers
volunteers_data = [
    {
        'name': 'Raj Kumar',
        'email': 'raj@example.com',
        'phone': '9876543210',
        'address': '123 Community Street, New Delhi',
        'skills': 'teaching',
        'availability': 'weekends',
        'status': 'active',
        'hours_contributed': 15.5,
        'bio': 'Passionate about education and mentoring young minds.'
    },
    {
        'name': 'Priya Sharma',
        'email': 'priya@example.com',
        'phone': '9876543211',
        'address': '456 Volunteer Lane, Mumbai',
        'skills': 'counseling',
        'availability': 'flexible',
        'status': 'active',
        'hours_contributed': 22.0,
        'bio': 'Experienced counselor dedicated to mental health awareness.'
    },
    {
        'name': 'Amit Patel',
        'email': 'amit@example.com',
        'phone': '9876543212',
        'address': '789 Service Road, Bangalore',
        'skills': 'coding',
        'availability': 'weekdays_evening',
        'status': 'active',
        'hours_contributed': 8.5,
        'bio': 'Software developer helping build tech for social good.'
    },
    {
        'name': 'Neha Singh',
        'email': 'neha@example.com',
        'phone': '9876543213',
        'address': '321 Hope Avenue, Pune',
        'skills': 'social_media',
        'availability': 'flexible',
        'status': 'pending',
        'hours_contributed': 0.0,
        'bio': 'Digital marketer looking to make social impact online.'
    },
    {
        'name': 'Vikram Verma',
        'email': 'vikram@example.com',
        'phone': '9876543214',
        'address': '654 Change Street, Chennai',
        'skills': 'event_planning',
        'availability': 'weekends',
        'status': 'active',
        'hours_contributed': 18.0,
        'bio': 'Experienced event organizer for community programs.'
    },
    {
        'name': 'Anjali Gupta',
        'email': 'anjali@example.com',
        'phone': '9876543215',
        'address': '987 Growth Drive, Hyderabad',
        'skills': 'graphic_design',
        'availability': 'flexible',
        'status': 'active',
        'hours_contributed': 12.0,
        'bio': 'Creative designer passionate about visual communication.'
    },
]

for vol_data in volunteers_data:
    try:
        volunteer = Volunteer.objects.create(**vol_data)
        print(f"[+] Volunteer created: {volunteer.name}")

        # Create user account
        try:
            user = User.objects.create_user(
                username=volunteer.email,
                email=volunteer.email,
                password='volunteer@123'
            )
            print(f"    [+] User account created for {volunteer.name}")
        except:
            print(f"    [!] User account already exists")

        # Create activity log
        ActivityLog.objects.create(
            volunteer=volunteer,
            activity_type='registration',
            description=f'Volunteer registered: {volunteer.name}',
            admin_user='system'
        )
    except Exception as e:
        print(f"[!] Error creating volunteer {vol_data['name']}: {e}")

print("\n[SUCCESS] Sample data setup complete!")
print("\nDemo Login Credentials:")
print("=" * 50)
print("ADMIN LOGIN:")
print("  Username: admin")
print("  Password: admin@123")
print("\nVOLUNTEER LOGIN (any of these):")
print("  Email: raj@example.com (password: volunteer@123)")
print("  Email: priya@example.com (password: volunteer@123)")
print("  Email: amit@example.com (password: volunteer@123)")
print("  Email: neha@example.com (password: volunteer@123)")
print("  Email: vikram@example.com (password: volunteer@123)")
print("  Email: anjali@example.com (password: volunteer@123)")
