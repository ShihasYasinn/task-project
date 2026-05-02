from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@login_required
def user_list(request):
    if request.user.role == 'associate':
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_detail(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    user_detail = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user_detail': user_detail})

@login_required
def user_create(request):
    if request.user.role == 'associate':
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form})

@login_required
def user_update(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'object': user})

@login_required
def user_delete(request, pk):
    if request.user.role == 'associate':
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user-list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})
