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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image_url = models.URLField(max_length=200, default=None)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.asin} [{self.domain}]"
    
class UserSettings(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('INR', 'Indian Rupees'),
        ('CAD', 'Canadian Dollar'),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0])
    discord = models.CharField(max_length=100, blank=True)
    change_per = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} settings'
