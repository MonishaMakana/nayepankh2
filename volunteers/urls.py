from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('volunteer/<int:pk>/', views.volunteer_profile, name='volunteer_profile'),
    path('volunteer/<int:pk>/edit/', views.volunteer_edit, name='volunteer_edit'),

    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/volunteers/', views.volunteer_list_admin, name='volunteer_list_admin'),
    path('admin/volunteer/<int:pk>/approve/', views.approve_volunteer, name='approve_volunteer'),
    path('admin/volunteer/<int:pk>/hours/', views.update_volunteer_hours, name='update_hours'),
    path('admin/reports/', views.generate_reports, name='generate_reports'),
    path('admin/export/csv/', views.export_volunteers_csv, name='export_csv'),
    path('admin/export/json/', views.export_reports_json, name='export_json'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
