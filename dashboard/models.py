from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ProductsDB(models.Model):
    COUNTRY_CHOICES = [
        ('COM', 'United States (com)'),
        ('UK', 'United Kingdom (uk)'),
        ('CA', 'Canada (ca)'),
        ('AU', 'Australia (au)'),
        ('DE', 'Germany (gr)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    asin = models.CharField(max_length=12)
    domain = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default='COM')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    last_checked_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.asin} [{self.domain}]"
    
class UserSettings(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('INR', 'Indian Rupees'),
        ('CAD', 'Canadian Dollar'),
        ]
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('discord', 'Discord'),
    ]
    notification_preference = models.CharField(
        max_length=7,
        choices=NOTIFICATION_CHOICES,
        default='email',
    )
    discord_webhook_url = models.URLField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0])
    change_per = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} settings'
