from django import forms
from .models import ProductsDB, UserSettings, NotificationPreference, CurrencyRate

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductsDB
        fields = ['asin','domain', 'title', 'price','image_url']

    domain = forms.ModelChoiceField(
        queryset=CurrencyRate.objects.all(),
        empty_label="Select Domain",
        # initial='http://amazon.com',
    )
    price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Price')
    title = forms.CharField(required=False, max_length=255, label='Title')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        
        print(f"User in Form: {user}")  # Debugging line to check user in form
        if user:
            try:
                user_settings = UserSettings.objects.get(user=user)
                self.fields['domain'].initial = user_settings.currency
            except UserSettings.DoesNotExist:
                pass


class SettingsForm(forms.ModelForm):
    notification_preference = forms.ModelMultipleChoiceField(
        queryset=NotificationPreference.objects.all(),
        required=False,
    )
    discord_webhook_url = forms.URLField(required=False)
    # currency = forms.ChoiceField(required=False, choices=)
    currency = forms.ModelChoiceField(
        queryset=CurrencyRate.objects.all(),
        empty_label="Select domain",
        required=False
    )
    change_per = forms.IntegerField(required=False)
    class Meta:
        model = UserSettings
        fields = ['notification_preference', 'discord_webhook_url', 'currency', 'change_per']



