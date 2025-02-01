from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {
        'customers': customers
    })

@login_required
def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Client ajouté avec succès.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Ajouter un client'
    })

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client modifié avec succès.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'customer': customer,
        'title': 'Modifier un client'
    })

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Client supprimé avec succès.')
    return redirect('customers:customer_list')