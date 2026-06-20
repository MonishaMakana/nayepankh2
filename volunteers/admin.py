from django.contrib import admin
from .models import Volunteer, VolunteerAdmin, ActivityLog, Report


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'skills', 'hours_contributed', 'registration_date']
    list_filter = ['status', 'skills', 'registration_date']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['registration_date', 'created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Volunteering Details', {
            'fields': ('skills', 'availability', 'bio', 'status')
        }),
        ('Hours & Activity', {
            'fields': ('hours_contributed', 'last_activity_date')
        }),
        ('Verification', {
            'fields': ('email_verified', 'verification_token')
        }),
        ('Timestamps', {
            'fields': ('registration_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'activity_type', 'created_at', 'admin_user']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['volunteer__name', 'description']
    readonly_fields = ['created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_date']
    list_filter = ['report_type', 'generated_date']
    search_fields = ['title', 'description']
    readonly_fields = ['generated_date']
