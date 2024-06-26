from .models import Notification

def notifications(request):
    unread_notification = Notification.objects.filter(is_read=False).values()
    return {
        'unread_notification': unread_notification
    }

def sidebar_menus(request):
    sidebar_menus = [
        ('Dashboard','dashboard','/dashboard/'),
        ('Add Product','add-product','/dashboard/add-product/'),
        ('View','view-products','/dashboard/view-products/'),
        ('Notifications', 'notifications','/dashboard/notifications/'),
        ('Profile', 'profile','/dashboard/profile/'),
        ('Settings', 'settings', '/dashboard/settings/'),
    ]
    return {
        'sidebar_menus': sidebar_menus,
    }