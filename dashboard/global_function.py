
def notifications(request):
    notifications = request.user.notifications.all()
    unread_notification = notifications.filter(is_read=False, user=request.user)
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