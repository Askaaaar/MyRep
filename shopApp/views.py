from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Product, History, User, Category
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import datetime
from .models import now
from dateutil.tz import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def homeview(request):
    return render(request, 'home.html', {'categories': Category.objects.all(),
                                         'products': Product.objects.all()})


def categoryview(request, categoryid):
    return render(request, 'category.html', {'products': Product.objects.filter(category=categoryid),
                                             'categories': Category.objects.all()})


def productview(request, productid):
    return render(request, 'product.html', {'products': Product.objects.get(id=productid),
                                            'categories': Category.objects.all()})


def productListView(request):
    return render(request, 'product_list.html', {'categories': Category.objects.all(),
                                                 'products': Product.objects.all()})


def companyView(request):
    return render(request, 'company.html', {'categories': Category.objects.all(),
                                            'products': Product.objects.all()})


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
        products_list = Product.objects.get(id=items)
        history.product.add(products_list)
    cart.clear()
    print(history)
    return redirect("home")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Пробное сообщение"
            body = {
                'Имя': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message,
                          'os.myworld@mail.ru',
                          ['os.myworld@mail.ru'])
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect("home")
    form = ContactForm()
    return render(request, "contact.html", {'form': form,
                                            'categories': Category.objects.all(),
                                            'products': Product.objects.all()})


@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


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
