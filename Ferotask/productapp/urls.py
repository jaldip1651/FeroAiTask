from django.urls import path
from productapp import views

urlpatterns = [
    path('customers', views.Customer_view.as_view(), name='get all customers'),
    path('customers/<int:pk>', views.Customer_view.as_view(), name='update customers'),
    path('products', views.Product_view.as_view(), name='get all products'),
    path('orders', views.Order_view.as_view(), name='get all orders'),
    path('orders/<int:pk>', views.Order_view.as_view(), name='update order'),
    path('orders/', views.OrderListByProducts.as_view(), name='orders_by_products'),
    path('customer_orders/', views.OrderListByCustomer.as_view(), name='orders_by_customer'),

]
