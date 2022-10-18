from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product, History, User, Category
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import datetime
from .models import now
from dateutil.tz import *


def homeview(request):
    return render(request, 'home.html', {'categories': Category.objects.all()})


def categoryview(request, categoryid):
    queryset = Product.objects.filter(category=categoryid),
    return render(request, 'category.html', {'products': queryset,
                                             'categories': Category.objects.all()})


def productview(request, productid):
    return render(request, 'product.html', {'object': Product.objects.get(id=productid),
                                            'categories': Category.objects.all()})


def products(request):
    return render(request, 'product_list.html', {'products': Product.objects.all()})


def payment(request):
    price = 0
    product = []
    cart = Cart(request)
    for item in cart.cart.values():
        product.append(item['product_id'])
        price += float(item['price']) * float(item['quantity'])
    history = History(
        total_price=price,
        data=datetime.datetime.now(tzlocal()).strftime("%Y-%m-%d %H:%M:%S"),
        user=User.objects.get(id=request.user.id))
    history.save()
    for items in product:
        product_list = Product.objects.get(id=items)
        history.product.add(product_list)
    cart.clear()
    print(history)
    return redirect("home")


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("product_list")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
