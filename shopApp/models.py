import datetime
from dateutil.tz import *
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django import forms

now = datetime.datetime.now(tzlocal())


class User(AbstractUser):
    phone = PhoneNumberField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    activation_code = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.username} {self.last_name}'


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, upload_to='category', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(null=True, upload_to='product', blank=True)
    stock = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])


class History(models.Model):
    product = models.ManyToManyField('Product')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    total_price = models.FloatField()
    data = models.DateTimeField(now.strftime("%Y-%m-%d %H:%M:%S"), null=True)


