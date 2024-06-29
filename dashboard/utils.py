# utils.py in the notifications app
from .models import Notification
from django.contrib.auth.models import User

def create_notification(user, product, notification_type, message):
    Notification.objects.create(
        user=user,
        product=product,
        notification_type=notification_type,
        message=message
    )