from .models import Notification

def notifications(request):
    try:
        unread_notification = Notification.objects.filter(is_read=False, user=request.user).values()
    except:
        unread_notification = []
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