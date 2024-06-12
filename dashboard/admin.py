from django.contrib import admin
from .models import ProductsDB
from .models import UserSettings

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'price', 'domain','user','date_added')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency','discord', 'change_per')

admin.site.register(ProductsDB, ProductsAdmin)
admin.site.register(UserSettings, SettingsAdmin)