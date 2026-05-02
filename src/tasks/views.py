from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Permission check for associates
    if request.user.role not in ['admin', 'supervisor']:
        if task.assignee != request.user:
            messages.error(request, "You do not have permission to edit this task.")
            return redirect('dashboard')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.task_code}" updated successfully.')
            if task.project:
                return redirect('project-detail', pk=task.project.pk)
            elif task.service:
                return redirect('service-detail', pk=task.service.pk)
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk if task.project else None
    service_pk = task.service.pk if task.service else None
    
    if request.method == 'POST':
        task_code = task.task_code
        task.delete()
        messages.success(request, f'Task "{task_code}" deleted successfully.')
        if project_pk:
            return redirect('project-detail', pk=project_pk)
        elif service_pk:
            return redirect('service-detail', pk=service_pk)
        return redirect('dashboard')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
