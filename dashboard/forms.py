from django import forms
from .models import ProductsDB, UserSettings, NotificationPreference, CurrencyRate

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductsDB
        fields = ['asin','domain', 'title', 'price','image_url']

    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Price')
    title = forms.CharField(required=False, max_length=255, label='Title')

# class SettingsForm(forms.ModelForm):
#     class Meta:
#         model = UserSettings
#         field = ['notification_preference', 'discord_webhook_url', 'currency', 'change_per']
    
#     discord_webhook_url = forms.URLField(required=False, max_length=200)
#     currency = forms.CharField(required=False)
#     notification_preference = forms.CharField()
#     change_per = forms.IntegerField(required=False)

class SettingsForm(forms.ModelForm):
    notification_preference = forms.ModelMultipleChoiceField(
        queryset=NotificationPreference.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    discord_webhook_url = forms.URLField(required=False)
    # currency = forms.ChoiceField(required=False, choices=)
    currency = forms.ModelChoiceField(
        queryset=CurrencyRate.objects.all(),
        empty_label="Select a currency",
        required=False
    )
    change_per = forms.IntegerField(required=False)
    class Meta:
        model = UserSettings
        fields = ['notification_preference', 'discord_webhook_url', 'currency', 'change_per']


