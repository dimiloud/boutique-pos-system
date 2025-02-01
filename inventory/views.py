from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from .utils import BarcodeGenerator

# ... Vos vues existantes ...

@login_required
def generate_barcode(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Générer l'étiquette
    image_buffer = BarcodeGenerator.generate_product_label(product)
    
    # Retourner l'image
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{product.sku}_barcode.png"'
    response.write(image_buffer.getvalue())
    
    return response

@login_required
def generate_multiple_barcodes(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        quantity = int(request.POST.get('quantity', 1))
        
        if not product_ids:
            messages.error(request, 'Aucun produit sélectionné')
            return redirect('inventory:product_list')
        
        # Créer un fichier ZIP avec toutes les étiquettes
        import zipfile
        from io import BytesIO
        
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for product_id in product_ids:
                product = get_object_or_404(Product, pk=product_id)
                for i in range(quantity):
                    image_buffer = BarcodeGenerator.generate_product_label(product)
                    zip_file.writestr(
                        f"{product.sku}_barcode_{i+1}.png",
                        image_buffer.getvalue()
                    )
        
        # Retourner le fichier ZIP
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="barcodes.zip"'
        response.write(zip_buffer.getvalue())
        
        return response
    
    # Si GET, afficher le formulaire de sélection
    products = Product.objects.filter(active=True)
    return render(request, 'inventory/generate_barcodes.html', {
        'products': products
    })