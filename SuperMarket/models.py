from django.db import models
from django.conf import settings
import random
from ckeditor.fields import RichTextField
from Account.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver



class Product(models.Model):

    Shop = models.ForeignKey(ShopAccount, on_delete=models.CASCADE, null=True)

    Categories = [
        ("Backyard", "Backyard"),
        ("Toys", "Toys"),
        ("Cosmetic", "Cosmetic"),
        ("Electronic", "Electronic"),
        ("Hobby", "Hobby"),
        ("Home", "Home"),
        ("Fashion", "Fashion"),
        ("Sports", "Sports"),
    ]

    Name = models.CharField(max_length=43, verbose_name="Product Name")
    Price = models.FloatField(verbose_name="Product Price")
    Description = RichTextField(verbose_name="Description")

    Category = models.CharField(choices=Categories, max_length=12)
    Brand = models.CharField(max_length=120)

    Photo1 = models.ImageField()
    Photo2 = models.ImageField()
    Photo3 = models.ImageField()
    Photo4 = models.ImageField()
    Photo5 = models.ImageField()

    UploadDate = models.DateField(verbose_name="Upload Date", auto_now_add=True)

    def __str__(self):
        return self.Name


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Name = models.CharField(max_length=120)
    Email = models.EmailField()
    Text = models.TextField()
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return  self.Name  + " " + "(" + self.product.Name + ")"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    totalPrice = models.FloatField(default=0)
    # Customer Infos
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # states
    isBuyed = models.BooleanField(default=False)
    isConfirmed = models.BooleanField(default=False)
    isShipping = models.BooleanField(default=False)
    cargoNumber = models.IntegerField(default=0)
    isFinished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.totalPrice = self.product.Price * self.count
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.Name + " -- Count: " + str(self.count)


class Order(models.Model):
    account = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    totalPrice = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.account.username + "Orders"

