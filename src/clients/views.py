from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Client
from .forms import ClientForm

@login_required
def client_list(request):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to access clients.")
        return redirect('dashboard')
    clients = Client.objects.all()
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) | 
            Q(surname__icontains=search_query) | 
            Q(client_code__icontains=search_query) |
            Q(friendly_name__icontains=search_query)
        )
        
    # Status Filter
    status_filter = request.GET.get('status', '')
    if status_filter and status_filter != 'All Status':
        clients = clients.filter(status=status_filter)
        
    # Pagination
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'clients': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'clients/client_list.html', context)

@login_required
def client_detail(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to access client details.")
        return redirect('dashboard')
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/client_detail.html', {'client': client})

@login_required
def client_create(request):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to create clients.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client-list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})

@login_required
def client_update(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to update clients.")
        return redirect('dashboard')
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form, 'object': client})

@login_required
def client_delete(request, pk):
    if request.user.role == 'associate':
        messages.error(request, "You do not have permission to delete clients.")
        return redirect('dashboard')
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client-list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})
