from django.contrib import admin
from .models import ProductsDB
from .models import UserSettings, NotificationPreference, CurrencyRate

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('asin', 'title', 'price', 'domain','user','last_checked')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'change_per', 'notification_preferences_display')

    def notification_preferences_display(self, obj):
        return ", ".join([preference.get_type_display() for preference in obj.notification_preference.all()])
    notification_preferences_display.short_description = 'Notification Preferences'

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('country', 'currency_name','currency_code', 'exchange_rate','domain_url')

admin.site.register(ProductsDB, ProductsAdmin)
admin.site.register(UserSettings, SettingsAdmin)
admin.site.register(NotificationPreference)
admin.site.register(CurrencyRate, CurrencyRateAdmin)