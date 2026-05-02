from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Service
from .forms import ServiceForm
from django.db.models import Q
from tasks.models import Task
from tasks.forms import TaskForm, ServiceTaskForm

@login_required
def service_list(request):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to access services.")
        return redirect('dashboard')
    services = Service.objects.all()
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Apply search filter
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | 
            Q(service_code__icontains=search_query)
        )
        
    # Apply status filter
    if status_filter and status_filter != 'All Status':
        services = services.filter(status=status_filter)
        
    # Pagination
    paginator = Paginator(services, 10) # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'services': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'services/service_list.html', context)

@login_required
def service_detail(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to access service details.")
        return redirect('dashboard')
    service = get_object_or_404(Service, pk=pk)
    tasks = service.service_tasks.all()
    
    if request.method == 'POST':
        task_form = ServiceTaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.service = service
            task.save()
            task_form.save_m2m()
            messages.success(request, f'Task "{task.title}" added to service.')
            return redirect('service-detail', pk=pk)
        else:
            messages.error(request, 'Error adding task. Please check the form.')
    else:
        task_form = ServiceTaskForm()
        
    context = {
        'service': service,
        'tasks': tasks,
        'task_form': task_form,
    }
    return render(request, 'services/service_detail.html', context)

@login_required
def service_create(request):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to create services.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            messages.success(request, f'Service "{service.name}" created successfully.')
            return redirect('service-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def service_update(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to update services.")
        return redirect('dashboard')
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.name}" updated successfully.')
            return redirect('service-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'object': service})

@login_required
def service_delete(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to delete services.")
        return redirect('dashboard')
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        name = service.name
        service.delete()
        messages.success(request, f'Service "{name}" deleted successfully.')
        return redirect('service-list')
    return render(request, 'services/service_confirm_delete.html', {'service': service})
