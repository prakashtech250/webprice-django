from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-product/', views.addProduct, name='add-product'),
    path('import-products/', views.import_products, name='import-products'),
    path('view-products/', views.viewProducts, name='view-products'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('notifications/', views.notifications, name="notifications"),
    path('product/<int:pk>/edit/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)