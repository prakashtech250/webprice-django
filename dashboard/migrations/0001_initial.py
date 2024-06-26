# Generated by Django 4.2.13 on 2024-06-17 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('currency_name', models.CharField(max_length=100)),
                ('currency_code', models.CharField(max_length=10)),
                ('exchange_rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('domain_url', models.URLField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('email', 'Email'), ('discord', 'Discord')], default='email', max_length=7, unique=True, verbose_name='Notification Type')),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_webhook_url', models.URLField(blank=True, null=True)),
                ('change_per', models.IntegerField(blank=True, default=0, null=True)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.currencyrate')),
                ('notification_preference', models.ManyToManyField(blank=True, to='dashboard.notificationpreference')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('asin', models.CharField(max_length=12)),
                ('domain', models.CharField(choices=[('COM', 'United States (com)'), ('UK', 'United Kingdom (uk)'), ('CA', 'Canada (ca)'), ('AU', 'Australia (au)'), ('DE', 'Germany (gr)')], default='COM', max_length=3)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('last_checked_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('last_checked', models.DateTimeField(auto_now=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
