from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('contact/', views.contact, name='contact'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-cart/<int:product_id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

]