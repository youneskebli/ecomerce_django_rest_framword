from django.urls import path
from . import views
urlpatterns = [
    path('orders/', views.get_all_orders,name='get_all_orders'),
    path('orders/<str:pk>',views.get_one_order,name='get_one_order'),
    path('orders/new/', views.create_order, name='create_order'),
    path('orders/update/<str:pk>', views.update_order_status, name='update_order_status'),
    path('orders/delete/<str:pk>', views.delete_order, name='delete_order')
]