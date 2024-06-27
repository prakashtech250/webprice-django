from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class CurrencyRate(models.Model):
    domain_code = models.CharField(max_length=5, blank=True, null=True)
    country = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    domain_url = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.domain_url}"
    
class ProductsDB(models.Model):
    COUNTRY_CHOICES = [
        ('COM', 'United States (com)'),
        ('UK', 'United Kingdom (uk)'),
        ('CA', 'Canada (ca)'),
        ('AU', 'Australia (au)'),
        ('DE', 'Germany (gr)'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    asin = models.CharField(max_length=12)
    # domain = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default='COM')
    domain = models.ForeignKey(CurrencyRate, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    last_checked_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.asin} [{self.domain}]"
    
class NotificationPreference(models.Model):
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('discord', 'Discord'),
    ]
    type = models.CharField(
        max_length=7,
        unique=True,
        choices=NOTIFICATION_CHOICES,
        verbose_name='Notification Type',
        default = 'email'
    )

    def __str__(self):
        return self.get_type_display()

class UserSettings(models.Model):
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('discord', 'Discord'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('INR', 'Indian Rupees'),
        ('CAD', 'Canadian Dollar'),
    ]
    notification_preference = models.ManyToManyField(NotificationPreference, blank=True)
    discord_webhook_url = models.URLField(blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.ForeignKey(CurrencyRate, on_delete=models.SET_NULL, null=True, blank=True)
    change_per = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} settings'
    

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('price_increase', 'Price Increase'),
        ('price_decrease', 'Price Decrease'),
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    product = models.ForeignKey(ProductsDB, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message[:20]}...'


