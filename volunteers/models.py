from django.db import models
from django.core.validators import EmailValidator, URLValidator
from django.utils import timezone

SKILLS_CHOICES = [
    ('teaching', 'Teaching'),
    ('counseling', 'Counseling'),
    ('mentoring', 'Mentoring'),
    ('coding', 'Coding'),
    ('graphic_design', 'Graphic Design'),
    ('content_writing', 'Content Writing'),
    ('event_planning', 'Event Planning'),
    ('fundraising', 'Fundraising'),
    ('social_media', 'Social Media'),
    ('other', 'Other'),
]

AVAILABILITY_CHOICES = [
    ('weekdays_morning', 'Weekdays (Morning)'),
    ('weekdays_evening', 'Weekdays (Evening)'),
    ('weekends', 'Weekends'),
    ('flexible', 'Flexible'),
]

VOLUNTEER_STATUS_CHOICES = [
    ('pending', 'Pending Approval'),
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('rejected', 'Rejected'),
]


class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    skills = models.CharField(
        max_length=50,
        choices=SKILLS_CHOICES,
        default='other'
    )
    availability = models.CharField(
        max_length=50,
        choices=AVAILABILITY_CHOICES,
        default='flexible'
    )
    bio = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=VOLUNTEER_STATUS_CHOICES,
        default='pending'
    )
    hours_contributed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registration_date']
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_approved(self):
        return self.status == 'active'

    @property
    def is_pending(self):
        return self.status == 'pending'


class VolunteerAdmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_superadmin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.name} ({self.email})"


class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('registration', 'Registration'),
        ('approval', 'Approval'),
        ('rejection', 'Rejection'),
        ('hours_update', 'Hours Update'),
        ('status_change', 'Status Change'),
        ('login', 'Login'),
    ]

    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_user = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f"{self.volunteer.name} - {self.activity_type}"


class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    generated_date = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('monthly', 'Monthly Report'),
            ('quarterly', 'Quarterly Report'),
            ('annual', 'Annual Report'),
            ('volunteer_stats', 'Volunteer Statistics'),
        ]
    )
    data = models.JSONField(default=dict)

    class Meta:
        ordering = ['-generated_date']

    def __str__(self):
        return f"{self.title} - {self.generated_date.strftime('%Y-%m-%d')}"
