from django.db import models


class Address(models.Model):
    Name = models.CharField(max_length=120)

    CountryList = (
        ("Turkey", "TR"),
        ("United States", "ABD"),
    )

    country = models.CharField(choices=CountryList, max_length=20)

    CityList = (
        ("Istanbul", "Istanbul"),
        ("Ankara", "Ankara"),
    )

    city = models.CharField(choices=CityList, max_length=50)

    TownList = (
        ("Beylikdüzü", "Beylikdüzü"),
        ("Keçiören", "Keçiören"),
    )

    town = models.CharField(choices=TownList, max_length=50)

    def __str__(self):
        return self.Name


class ShopAccount(models.Model):
    ShopName = models.CharField(max_length=80, verbose_name="Shop Name")
    Addres = models.TextField()
    Email = models.EmailField()
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address, blank=True)

    def __str__(self):
        return self.ShopName


class CustomerAccount(models.Model):
    Name = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100, verbose_name="Last Name")
    Email = models.EmailField()
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address, blank=True)

    def __str__(self):
        return self.user.username



def findAccount(user):
    try:
        isShop = ShopAccount.objects.get(user=user)
    except Exception as e:
        isShop = None

    try:
        isCustomer = CustomerAccount.objects.get(user=user)
    except Exception as e:
        isCustomer = None

    if isShop:
        return isShop

    elif isCustomer:
        return isCustomer
