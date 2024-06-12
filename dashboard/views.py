from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductsDB
from .forms import ProductForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from .scrapers import get_data


# Create your views here.

sidebar_menus = [
    ('Dashboard','dashboard','/dashboard/'),
    ('Add Product','add-product','/dashboard/add-product/'),
    ('View','view-products','/dashboard/view-products/'),
    ('Profile', 'profile','/dashboard/profile/'),
    ('Settings', 'settings', '/dashboard/settings/'),
]

@login_required
def dashboard(request):
    all_products = ProductsDB.objects.filter()
    totalProducts = len(all_products)
    return render(request, 'index1.html', {'menus': sidebar_menus, 'totalProducts': totalProducts})

@login_required
def addProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if 'submit' in request.POST:
            if form.is_valid():
                product = form.save(commit=False)
                product.user = request.user
                try:
                    product.save()
                    messages.success(request, f"Product {product.asin} is added successfully. ")
                    return redirect('add-product')  # Replace with your success URL
                except Exception as e:
                    messages.error(request, 'Something went wrong while saving product')
            else:
                messages.error(request, 'Something went wrong while adding product.')
        elif 'get_info' in request.POST:
            asin = request.POST.get('asin')
            domain = request.POST.get('domain').lower()
            if asin and domain:
                product_info = {'asin': asin, 'title': 'this is some random title', 'price': 2.1}
                product_info = get_data(asin, domain)
                if product_info:
                    form = ProductForm(initial=product_info)
                    messages.success(request, 'Product information retrieved successfully.')
                else:
                    messages.error(request, 'Failed to retrieve product information. Please check the ASIN and country code.')
            else:
                messages.error(request, 'ASIN and country are required to get product information.')
                
    else:
        form = ProductForm()
    return render(request, 'add-product.html', {'menus': sidebar_menus, 'form': form})

@login_required
def viewProducts(request):
    # all_products = ProductsDB.objects.filter(username=request.user.username)
    all_products = ProductsDB.objects.all()
    paginator = Paginator(all_products, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'view-products.html', {'menus': sidebar_menus, 'all_products': page_obj, 'total_product':len(all_products)})

@login_required
def profile(request):
    userDetails = request.user
    return render(request, 'profile.html', {'menus': sidebar_menus, 'user': userDetails})

@login_required
def settings(request):
    return render(request, 'settings.html', {'menus': sidebar_menus})


@login_required
def update_product(request, pk):
    product = get_object_or_404(ProductsDB, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            pass
    else:
        pass
    pass


@login_required
def delete_product(request, pk):
    product = get_object_or_404(ProductsDB, pk=pk)
    print(product)
    print(request)
    print(pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'{product.asin} is deleted.')
    return redirect('view-products')

