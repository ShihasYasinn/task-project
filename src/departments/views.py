from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Department
from .forms import DepartmentForm

@login_required
def department_list(request):
    if request.user.role == 'associate':
        return redirect('dashboard')
    departments = Department.objects.all()
    return render(request, 'departments/department_list.html', {'departments': departments})

@login_required
def department_detail(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'departments/department_detail.html', {'department': department})

@login_required
def department_create(request):
    if request.user.role == 'associate':
        return redirect('dashboard')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/department_form.html', {'form': form})

@login_required
def department_update(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department-list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department_form.html', {'form': form, 'object': department})

@login_required
def department_delete(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department-list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})
