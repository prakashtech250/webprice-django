from django import forms
from .models import ProductsDB

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductsDB
        fields = ['asin','domain', 'title', 'price','image_url']

    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Price')
    title = forms.CharField(required=False, max_length=255, label='Title')