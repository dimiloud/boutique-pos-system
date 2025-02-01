from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm, POSItemForm
from inventory.models import Product

@login_required
def dashboard(request):
    # Statistiques du jour
    today = timezone.now().date()
    sales_today = Sale.objects.filter(date__date=today)
    
    context = {
        'total_sales_today': sales_today.aggregate(Sum('total'))['total__sum'] or 0,
        'num_sales_today': sales_today.count(),
        'avg_sale_today': (sales_today.aggregate(Sum('total'))['total__sum'] or 0) / max(sales_today.count(), 1),
        'top_products': SaleItem.objects.filter(sale__date__date=today)
                                .values('product__name')
                                .annotate(total_quantity=Sum('quantity'))
                                .order_by('-total_quantity')[:5],
    }
    return render(request, 'sales/dashboard.html', context)

@login_required
def pos(request):
    if request.method == 'POST':
        form = POSItemForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            
            if barcode and not product:
                try:
                    product = Product.objects.get(barcode=barcode)
                except Product.DoesNotExist:
                    messages.error(request, 'Produit non trouvé')
                    return redirect('sales:pos')
            
            # Ajouter au panier en session
            cart = request.session.get('cart', [])
            cart.append({
                'product_id': product.id,
                'name': product.name,
                'quantity': quantity,
                'price': str(product.price),
                'total': str(product.price * quantity)
            })
            request.session['cart'] = cart
            
            messages.success(request, 'Produit ajouté au panier')
            return redirect('sales:pos')
    else:
        form = POSItemForm()
    
    # Récupérer le panier de la session
    cart = request.session.get('cart', [])
    total = sum(float(item['total']) for item in cart)
    
    return render(request, 'sales/pos.html', {
        'form': form,
        'cart': cart,
        'total': total
    })

@login_required
def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales/sale_list.html', {
        'sales': sales
    })

@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {
        'sale': sale
    })