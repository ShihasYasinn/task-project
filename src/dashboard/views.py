from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from departments.models import Department
from services.models import Service
from clients.models import Client
from tasks.models import Task

@login_required
def dashboard_view(request):
    user = request.user
    
    if user.role in ['admin', 'supervisor']:
        tasks = Task.objects.all()
    else:
        # Associates and others only see their assigned tasks
        tasks = Task.objects.filter(assignee=user)
    
    context = {
        'total_users': User.objects.count(),
        'total_departments': Department.objects.count(),
        'total_services': Service.objects.count(),
        'total_clients': Client.objects.count(),
        'total_tasks_count': tasks.count(),
        'pending_tasks_count': tasks.filter(status__in=['pending', 'overdue']).count(),
        'live_tasks_count': tasks.filter(status__in=['open', 'in-progress']).count(),
        'overdue_tasks_count': tasks.filter(status='overdue').count(),
        'recent_tasks': tasks.order_by('-id')[:10],
        'is_associate': user.role not in ['admin', 'supervisor'],
    }
    return render(request, 'dashboard/index.html', context)
