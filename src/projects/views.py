from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project
from .forms import ProjectForm
from tasks.models import Task
from tasks.forms import TaskForm
from .utils import generate_project_tasks

@login_required
def project_list(request):
    user = request.user
    if user.role in ['admin', 'supervisor']:
        projects = Project.objects.all()
    else:
        # Associates only see projects assigned to them OR where they have assigned tasks
        projects = Project.objects.filter(
            Q(assignee=user) | Q(tasks__assignee=user)
        ).distinct()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(project_code__icontains=search_query) | 
            Q(friendly_name__icontains=search_query) |
            Q(service__name__icontains=search_query) |
            Q(client__name__icontains=search_query)
        )
        
    # Status Filter
    status_filter = request.GET.get('status', 'open')
    if status_filter and status_filter != 'All Status':
        projects = projects.filter(status=status_filter)
        
    # Pagination
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Permission check for associates
    if request.user.role not in ['admin', 'supervisor']:
        is_involved = project.assignee == request.user or project.tasks.filter(assignee=request.user).exists()
        if not is_involved:
            messages.error(request, "You do not have permission to view this project.")
            return redirect('dashboard')

    tasks_list = project.tasks.all()
    
    # If associate, only show their assigned tasks
    if request.user.role not in ['admin', 'supervisor']:
        tasks_list = tasks_list.filter(assignee=request.user)
    
    # Pagination
    paginator = Paginator(tasks_list, 15)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    
    if request.method == 'POST':
        if request.user.role == 'associate':
            messages.error(request, "You do not have permission to create tasks.")
            return redirect('project-detail', pk=pk)
            
        task_form = TaskForm(request.POST, user=request.user)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f'Task "{task.title}" added to project.')
            return redirect('project-detail', pk=pk)
        else:
            messages.error(request, "Error adding task. Please check the form.")
    else:
        task_form = TaskForm(user=request.user)
        
    context = {
        'project': project,
        'tasks': tasks,
        'task_form': task_form,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_create(request):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to create projects.")
        return redirect('project-list')
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            generate_project_tasks(project)
            messages.success(request, f'Project "{project.project_code}" created successfully.')
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_update(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to update projects.")
        return redirect('project-list')
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            generate_project_tasks(project)
            messages.success(request, f'Project "{project.project_code}" updated.')
            return redirect('project-list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'object': project})

@login_required
def project_delete(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to delete projects.")
        return redirect('project-list')
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        code = project.project_code
        project.delete()
        messages.success(request, f'Project "{code}" deleted.')
        return redirect('project-list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
