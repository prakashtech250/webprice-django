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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            try:
                user_settings = UserSettings.objects.get(user=self.user)
                self.fields['domain'].initial = user_settings.currency
            except UserSettings.DoesNotExist:
                pass

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.user = self.user
        if commit:
            product.save()
        return product


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


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Upload a CSV file containing product data.',
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )




