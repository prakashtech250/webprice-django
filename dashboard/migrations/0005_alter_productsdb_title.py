# Generated by Django 4.2.13 on 2024-06-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_productsdb_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsdb',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]