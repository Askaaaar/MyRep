from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('products_list/', views.products, name='products'),
    path('product/<int:pk>/', views.productview, name='product'),
    path('', views.homeview, name='home'),
    path('category/<int:categoryid>/', views.categoryview, name='category'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('payment', views.payment, name='payment'),
]
