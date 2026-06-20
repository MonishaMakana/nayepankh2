from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import csv
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Volunteer, ActivityLog, Report, VOLUNTEER_STATUS_CHOICES
from .forms import (
    VolunteerRegistrationForm, VolunteerLoginForm, VolunteerUpdateForm,
    VolunteerSearchForm, HoursUpdateForm, AdminApprovalForm
)


def home(request):
    total_volunteers = Volunteer.objects.count()
    active_volunteers = Volunteer.objects.filter(status='active').count()
    total_hours = Volunteer.objects.aggregate(Sum('hours_contributed'))['hours_contributed__sum'] or 0

    context = {
        'total_volunteers': total_volunteers,
        'active_volunteers': active_volunteers,
        'total_hours': total_hours,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            volunteer = form.save(commit=False)
            volunteer.email_verified = False
            volunteer.status = 'pending'
            volunteer.save()

            try:
                user = User.objects.create_user(
                    username=volunteer.email,
                    email=volunteer.email,
                    password=password
                )
                messages.success(request, 'Registration successful! Your application is pending admin approval.')
                ActivityLog.objects.create(
                    volunteer=volunteer,
                    activity_type='registration',
                    description=f'Volunteer registered: {volunteer.name}'
                )
                return redirect('login')
            except Exception as e:
                volunteer.delete()
                messages.error(request, f'Error creating user account: {str(e)}')
                return redirect('register')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = VolunteerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                volunteer = Volunteer.objects.get(email=email)
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    login(request, user)
                    ActivityLog.objects.create(
                        volunteer=volunteer,
                        activity_type='login',
                        description='Volunteer logged in'
                    )
                    messages.success(request, 'Logged in successfully!')
                    return redirect('volunteer_profile', pk=volunteer.id)
                else:
                    messages.error(request, 'Invalid email or password.')
            except Volunteer.DoesNotExist:
                messages.error(request, 'No volunteer found with this email.')
    else:
        form = VolunteerLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required(login_url='login')
def volunteer_profile(request, pk):
    volunteer = get_object_or_404(Volunteer, id=pk)

    if request.user.email != volunteer.email and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this profile.')
        return redirect('home')

    activity_logs = volunteer.activity_logs.all()[:10]

    context = {
        'volunteer': volunteer,
        'activity_logs': activity_logs,
        'hours': volunteer.hours_contributed,
    }
    return render(request, 'volunteer_profile.html', context)


@login_required(login_url='login')
def volunteer_edit(request, pk):
    volunteer = get_object_or_404(Volunteer, id=pk)

    if request.user.email != volunteer.email and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this profile.')
        return redirect('home')

    if request.method == 'POST':
        form = VolunteerUpdateForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('volunteer_profile', pk=volunteer.id)
    else:
        form = VolunteerUpdateForm(instance=volunteer)

    return render(request, 'volunteer_edit.html', {'form': form, 'volunteer': volunteer})


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Admin login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    pending_volunteers = Volunteer.objects.filter(status='pending')
    active_volunteers = Volunteer.objects.filter(status='active')
    total_volunteers = Volunteer.objects.count()

    stats = {
        'total': total_volunteers,
        'pending': pending_volunteers.count(),
        'active': active_volunteers.count(),
        'inactive': Volunteer.objects.filter(status='inactive').count(),
        'total_hours': Volunteer.objects.aggregate(Sum('hours_contributed'))['hours_contributed__sum'] or 0,
    }

    context = {
        'pending_volunteers': pending_volunteers,
        'active_volunteers': active_volunteers,
        'stats': stats,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='admin_login')
def volunteer_list_admin(request):
    if not request.user.is_staff:
        return redirect('home')

    form = VolunteerSearchForm(request.GET or None)
    volunteers = Volunteer.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        status = form.cleaned_data.get('status')
        skills = form.cleaned_data.get('skills')

        if search:
            volunteers = volunteers.filter(
                Q(name__icontains=search) | Q(email__icontains=search)
            )
        if status:
            volunteers = volunteers.filter(status=status)
        if skills:
            volunteers = volunteers.filter(skills=skills)

    context = {
        'volunteers': volunteers,
        'form': form,
    }
    return render(request, 'volunteer_list_admin.html', context)


@login_required(login_url='admin_login')
@require_http_methods(["POST"])
def approve_volunteer(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    volunteer = get_object_or_404(Volunteer, id=pk)
    form = AdminApprovalForm(request.POST)

    if form.is_valid():
        action = form.cleaned_data.get('action')
        comments = form.cleaned_data.get('comments', '')

        if action == 'approve':
            volunteer.status = 'active'
            activity_msg = 'Volunteer approved'
        else:
            volunteer.status = 'rejected'
            activity_msg = 'Volunteer rejected'

        volunteer.save()
        ActivityLog.objects.create(
            volunteer=volunteer,
            activity_type='approval' if action == 'approve' else 'rejection',
            description=f'{activity_msg}: {comments}' if comments else activity_msg,
            admin_user=request.user.username
        )
        messages.success(request, f'Volunteer {action}d successfully!')

    return redirect('volunteer_list_admin')


@login_required(login_url='admin_login')
def update_volunteer_hours(request, pk):
    if not request.user.is_staff:
        return redirect('home')

    volunteer = get_object_or_404(Volunteer, id=pk)

    if request.method == 'POST':
        form = HoursUpdateForm(request.POST)
        if form.is_valid():
            hours = form.cleaned_data.get('hours')
            description = form.cleaned_data.get('description')

            volunteer.hours_contributed += hours
            volunteer.last_activity_date = timezone.now()
            volunteer.save()

            ActivityLog.objects.create(
                volunteer=volunteer,
                activity_type='hours_update',
                description=f'Hours updated: +{hours} - {description}',
                admin_user=request.user.username
            )
            messages.success(request, 'Hours updated successfully!')
            return redirect('volunteer_profile', pk=volunteer.id)
    else:
        form = HoursUpdateForm()

    return render(request, 'update_hours.html', {'form': form, 'volunteer': volunteer})


@login_required(login_url='admin_login')
def generate_reports(request):
    if not request.user.is_staff:
        return redirect('home')

    total_volunteers = Volunteer.objects.count()
    active_volunteers = Volunteer.objects.filter(status='active').count()
    pending_volunteers = Volunteer.objects.filter(status='pending').count()
    total_hours = Volunteer.objects.aggregate(Sum('hours_contributed'))['hours_contributed__sum'] or 0

    skills_distribution = {}
    for vol in Volunteer.objects.all():
        skill = vol.get_skills_display()
        skills_distribution[skill] = skills_distribution.get(skill, 0) + 1

    top_volunteers = Volunteer.objects.filter(status='active').order_by('-hours_contributed')[:10]

    context = {
        'total_volunteers': total_volunteers,
        'active_volunteers': active_volunteers,
        'pending_volunteers': pending_volunteers,
        'total_hours': total_hours,
        'skills_distribution': skills_distribution,
        'top_volunteers': top_volunteers,
    }
    return render(request, 'reports.html', context)


@login_required(login_url='admin_login')
def export_volunteers_csv(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="volunteers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', 'Status', 'Skills', 'Hours Contributed', 'Registration Date'])

    for volunteer in Volunteer.objects.all():
        writer.writerow([
            volunteer.name,
            volunteer.email,
            volunteer.phone,
            volunteer.get_status_display(),
            volunteer.get_skills_display(),
            volunteer.hours_contributed,
            volunteer.registration_date.strftime('%Y-%m-%d'),
        ])

    return response


@login_required(login_url='admin_login')
def export_reports_json(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    data = {
        'total_volunteers': Volunteer.objects.count(),
        'active_volunteers': Volunteer.objects.filter(status='active').count(),
        'total_hours': float(Volunteer.objects.aggregate(Sum('hours_contributed'))['hours_contributed__sum'] or 0),
        'generated_date': timezone.now().isoformat(),
    }

    return JsonResponse(data)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
