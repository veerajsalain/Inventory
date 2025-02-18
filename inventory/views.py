from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Sale
from django.contrib import messages

def product_list(request):
    products = Product.objects.all()
    
    low_stock_products = Product.objects.filter(stock__lte=5)
    if low_stock_products.exists():
        messages.warning(request, "Some products are low in stock!")
    return render(request, 'inventory/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        stock = request.POST['stock']
        description = request.POST.get('description', '')

        Product.objects.create(name=name, price=price, stock=stock, description=description)
        messages.success(request, "Product added successfully!")
        return redirect('product_list')

    return render(request, 'inventory/add_product.html')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('product_list')

# def billing(request, sale_id):
#     sale = get_object_or_404(Sale, id=sale_id)
#     return render(request, 'inventory/billing.html', {'sale': sale})

def sell_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        if product.stock >= quantity:
            total_price = product.price * quantity
            sale= Sale.objects.create(product=product, quantity=quantity, total_price=total_price)
            product.stock -= quantity
            product.save()
            messages.success(request, f"Sold {quantity} {product.name}(s)")
            messages.success(request, "Sale recorded successfully")
            # return redirect('product_list')
            return redirect('billing', sale_id=sale.id) 
        else:
            messages.error(request, "Not enough stock!")

    return render(request, 'inventory/sell.html', {'product': product})

def add_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        added_stock = int(request.POST['added_stock'])
        product.stock += added_stock
        product.save()
        messages.success(request, f"Added {added_stock} units to {product.name}. New stock: {product.stock}")
        return redirect('product_list')

    return render(request, 'inventory/add_stock.html', {'product': product})
    

def sales_history(request):
    sales = Sale.objects.all()
    return render(request, 'inventory/sales_history.html', {'sales': sales})

def billing(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'inventory/billing.html', {'sale': sale})

def low_stock_alert(request):
    low_stock_products = Product.objects.filter(stock__lte=5)
    return render(request, 'inventory/low_stock.html', {'low_stock_products': low_stock_products})


