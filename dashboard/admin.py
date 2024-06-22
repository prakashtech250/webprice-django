from django.contrib import admin
from .models import ProductsDB
from .models import UserSettings, NotificationPreference, CurrencyRate, Notification

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'price', 'last_checked_price' ,'domain','user','last_checked')
    search_fields = ('asin', 'user')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'change_per', 'notification_preferences_display')

    def notification_preferences_display(self, obj):
        return ", ".join([preference.get_type_display() for preference in obj.notification_preference.all()])
    notification_preferences_display.short_description = 'Notification Preferences'

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency_name','currency_code', 'exchange_rate','domain_url')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'message', 'notification_type', 'is_read', 'created_at')
    # list_filter = ('notification_type', 'is_read', 'created_at')
    # search_fields = ('user__username', 'product__name', 'message')

admin.site.register(ProductsDB, ProductsAdmin)
admin.site.register(UserSettings, SettingsAdmin)
admin.site.register(NotificationPreference)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(Notification, NotificationAdmin)