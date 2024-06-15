from django.contrib import admin
from .models import ProductsDB
from .models import UserSettings

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'price', 'domain','user','last_checked')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency','discord_webhook_url','notification_preference','change_per')

admin.site.register(ProductsDB, ProductsAdmin)
admin.site.register(UserSettings, SettingsAdmin)