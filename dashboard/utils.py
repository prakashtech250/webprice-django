from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email(subject, message, from_email, recipient_list):
    html_content = render_to_string('email_template.html', {'subject': subject, 'message': message})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
    
def create_notification(user, product, notification_type, message):
    from .models import Notification
    Notification.objects.create(
        user=user,
        product=product,
        notification_type=notification_type,
        message=message
    )