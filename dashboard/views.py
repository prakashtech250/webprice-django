from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductsDB, UserSettings, CurrencyRate, Notification
from .forms import ProductForm, SettingsForm, CSVUploadForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.conf import settings as sett
import pytz

from .scrapers import get_data
from .discord_notify import send_notification
import pandas as pd
from io import StringIO


# Create your views here.

sidebar_menus = [
    ('Dashboard','dashboard','/dashboard/'),
    ('Add Product','add-product','/dashboard/add-product/'),
    ('View','view-products','/dashboard/view-products/'),
    ('Notifications', 'notifications','/dashboard/notifications/'),
    ('Profile', 'profile','/dashboard/profile/'),
    ('Settings', 'settings', '/dashboard/settings/'),
]

@login_required
def dashboard(request):
    all_products = ProductsDB.objects.filter(user=request.user).order_by('-date_added').values()
    unread_notification = Notification.objects.filter(is_read=False).values()
    for p in all_products:
        domain_url = CurrencyRate.objects.get(id=p['domain_id']).domain_url
        p['domain'] = domain_url.replace('https://www.','').strip()
    return render(request, 'index1.html', {'menus': sidebar_menus, 'all_products': all_products})

@login_required
def addProduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST, user=request.user)
        if 'submit' in request.POST:
            if form.is_valid():
                product = form.save(commit=False)
                product_found = ProductsDB.objects.filter(user=request.user, asin=product.asin, domain=product.domain).all()
                if not product_found:
                    product.user = request.user
                    try:
                        product.save()
                        messages.success(request, f"Product {product.asin} is added successfully. ")
                        return redirect('add-product')  # Replace with your success URL
                    except Exception as e:
                        print(f'Error: {e}')
                        messages.error(request, 'Something went wrong while saving product')
                else:
                    messages.error(request, f'Product {product.asin} is already added')
            else:
                messages.error(request, 'Something went wrong while adding product.')
        elif 'get_info' in request.POST:
            if form.is_valid():
                asin = request.POST.get('asin')
                domain_id = request.POST.get('domain').lower()
                domain = CurrencyRate.objects.get(id=domain_id).domain_url
                if asin and domain:
                    product_info = get_data(asin, domain)
                    product_info['domain'] = domain_id
                    if product_info:
                        form = ProductForm(initial=product_info, user=request.user)
                        if product_info['title'] or product_info['price'] or product_info['image_url']:
                            messages.success(request, 'Product information retrieved successfully.')
                        else:
                            messages.info(request, 'Product might be out of stock. Submit this product if you want to get notified')
                    else:
                        form = ProductForm(user=request.user)
                        messages.error(request, 'Failed to retrieve product information. Please check the ASIN and country code.')
                else:
                    messages.error(request, 'ASIN and country are required to get product information.')
                    
    else:
        form = ProductForm(user=request.user)
    return render(request, 'add-product.html', {'menus': sidebar_menus, 'form': form})

@login_required
def viewProducts(request): #
    all_products = ProductsDB.objects.filter(user=request.user).order_by('-date_added').values()
    for p in all_products:
        domain_url = CurrencyRate.objects.get(id=p['domain_id']).domain_url
        p['domain'] = domain_url.replace('https://www.','').strip()
    paginator = Paginator(all_products, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'view-products.html', {'menus': sidebar_menus, 'all_products': page_obj, 'total_product':len(all_products)})

@login_required
def profile(request):
    userDetails = request.user
    return render(request, 'profile.html', {'menus': sidebar_menus, 'user': userDetails})

@login_required
def settings(request):
    user = request.user
    user_settings = get_object_or_404(UserSettings, user=user)
    if request.method == "POST":
        if 'submit' in request.POST:
            form = SettingsForm(request.POST, instance=user_settings)
            if form.is_valid():
                new_settings = form.save()
                new_settings.user = request.user
                new_settings.save()
                messages.success(request, 'New Setting is saved.')
                return redirect('settings')
            else:
                print('form is not valid')
        elif 'check' in request.POST:
            form = SettingsForm(request.POST, instance=user_settings)
            discord_webhook_url = request.POST.get('discord_webhook_url')
            if discord_webhook_url:
                if form.is_valid():
                    userSettings = dict()
                    userSettings['discord_webhook_url'] = discord_webhook_url
                    form = SettingsForm(initial=userSettings)
                    notified = send_notification(discord_webhook_url)
                    if notified:
                        messages.success(request, 'Check your discord channel to verify')
                    else:
                        messages.error(request, 'Something wrong. Please check your discord webhook url')
                else:
                    messages.error(request, 'Webhook url is not valid')
            else:
                messages.error(request, 'Please enter discord webhook url')
        elif 'edit' in request.POST:
            messages.error(request, 'Something wrong')
            return redirect('settings')
    else:
        form = SettingsForm(instance=user_settings)
    return render(request, 'settings.html', {'menus': sidebar_menus, 'form': form})


@login_required
def update_product(request, pk):
    product = get_object_or_404(ProductsDB, id=pk)
    print('product found:', product)
    if product:
        if request.method == 'POST':
            print('post method')
            form = ProductForm(request.POST, instance=product)
            if 'submit' in request.POST:
                if form.is_valid():
                    product = form.save(commit=False)
                    product.user = request.user
                    product.save()
                    messages.success(request, 'Product is updated')
                    return redirect('view-products')
                else:
                    messages.error(request, 'Form is not valid')
            elif 'get_info' in request.POST:
                if form.is_valid():
                    asin = request.POST.get('asin')
                    domain_id = form.cleaned_data['domain'].id
                    domain = CurrencyRate.objects.get(id=domain_id)
                    domain_url = domain.domain_url
                    if asin and domain:
                        product_info = get_data(asin, domain_url)
                        product_info['domain'] = domain
                        if product_info:
                            form = ProductForm(initial=product_info)
                            messages.success(request, 'Product information retrieved successfully.')
                        else:
                            messages.error(request, 'Failed to retrieve product information. Please check the ASIN and country code.')
                    else:
                        messages.error(request, 'ASIN and country are required to get product information.')
                else:
                    messages.error(request, 'Form is not valid')
        else:
            form = ProductForm(instance=product)
            # print(form.asin)
    else:
        messages.error(request, 'Error on getting product')
    return render(request, 'add-product.html', {'menus': sidebar_menus, 'form': form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(ProductsDB, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'{product.asin} is deleted.')
    return redirect('view-products')

@login_required
def notifications(request):
    tz = pytz.timezone(sett.TIME_ZONE)
    now = timezone.now().astimezone(tz)
    today = now.date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    notifications = request.user.notifications.all().order_by('-created_at')
    today_notifications = notifications.filter(created_at__date=today, user=request.user)
    yesterday_notifications = notifications.filter(created_at__date=yesterday, user=request.user)
    last_week_notifications = notifications.filter(created_at__date__gte=last_week, created_at__date__lt=yesterday, user=request.user)
    last_month_notifications = notifications.filter(created_at__date__gte=last_month, created_at__date__lt=last_week, user=request.user)
    older_notifications = notifications.filter(created_at__date__lt=last_month, user= request.user)

    context = {
        "menus": sidebar_menus,
        'today_notifications': today_notifications,
        'yesterday_notifications': yesterday_notifications,
        'last_week_notifications': last_week_notifications,
        'last_month_notifications': last_month_notifications,
        'older_notifications': older_notifications,
    }
    return render(request, 'notifications.html', context)

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def mark_all_as_read(request):
    unread_notifications = request.user.notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)
    return redirect('notifications')

@login_required
def import_products(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = StringIO(csv_file.read().decode('utf-8'))
            df = pd.read_csv(csv_data)

            success_count = 0
            error_count = 0
            for _, row in df.iterrows():
                data = {
                    'asin': row.get('asin'),
                    'domain': row.get('domain'),
                    'title': row.get('title'),
                    'price': row.get('price'),
                    'image_url': row.get('image_url'),
                }

                product_form = ProductForm(data=data, user=request.user)
                if product_form.is_valid():
                    product = product_form.save(commit=False)
                    product.user = request.user
                    product.save()
                    success_count += 1
                else:
                    error_count += 1

            if success_count > 0:
                messages.success(request, f"Successfully imported {success_count} products.")
            if error_count > 0:
                messages.error(request, f"Failed to import {error_count} products.")
                
            return redirect('import-products')
        else:
            messages.error(request, "Failed to import products.")
    else:
        form = CSVUploadForm()
    return render(request, 'import-products.html', {'form': form})

