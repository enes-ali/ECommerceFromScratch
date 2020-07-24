from django.shortcuts import render, get_object_or_404, redirect
from django.http import response
from .models import *
from django.views.generic import View
from .forms import *
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from Account.models import findAccount
from django.core.paginator import Paginator


# Home Page
def HomeView(request):
    ShowcaseProducts = Product.objects.all()

    # Get Querys
    categoryQuery = request.GET.get("category")
    searchQuery = request.GET.get("q")

    if categoryQuery:
        products = Product.objects.filter(Category=categoryQuery)

        paginator = Paginator(products, 32)
        pageNum = request.GET.get("page")
        try:
            page = paginator.page(pageNum)
        except Exception as e:
            page = paginator.page(1)

        RenderData = {"showcase": page}

    elif searchQuery:
        queryProducts = Product.objects.filter(Name__icontains=searchQuery)
        paginator = Paginator(queryProducts, 32)
        pageNum = request.GET.get("page")
        try:
            page = paginator.page(pageNum)
        except Exception as e:
            page = paginator.page(1)

        RenderData = {"showcase": page}

    else:
        # Pageing
        paginator = Paginator(ShowcaseProducts, 32)
        pageNum = request.GET.get("page")
        try:
            page = paginator.page(pageNum)
        except Exception as e:
            page = paginator.page(1)
        RenderData = {"showcase": page}

    # Auth
    if (request.user.is_authenticated):
        cart = get_object_or_404(Order, account=request.user)
        total = 0
        for item in cart.items.all():
            total += item.product.Price
        cart.totalPrice = total
        cart.save()
        account = findAccount(request.user)
        RenderData['shopCart'] = cart
        RenderData['account'] = account

    return render(request, "index.html", RenderData)


# Product Page
class DetailView(View):

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        account = findAccount(request.user)
        comments = ProductComment.objects.filter(product=product)
        data = {"product": product, "account": account, "comments": comments}
        if (request.user.is_authenticated):
            cart = get_object_or_404(Order, account=request.user)
            total = 0
            for item in cart.items.all():
                total += item.product.Price
            cart.totalPrice = total
            cart.save()
            data['shopCart'] = cart
        return render(request, "detail.html", data)

    def post(self, request, id):
        product = Product.objects.get(id=id)
        count = int(request.POST["count"])
        addressId = int(request.POST["address"])
        address = Address.objects.get(id=addressId)
        orderItem = OrderItem.objects.create(product=product, count=count, address=address, customer=request.user)
        orderItem.save()
        order = Order.objects.get(account=request.user)
        order.items.add(orderItem)
        order.save()
        return redirect("home")

class addAddressView(View):

    def get(self, request):
        form = AddressForm(None)
        data = {"form":form}
        return render(request, "add_address.html", data)

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            account = findAccount(request.user)
            form.save()
            name = form.cleaned_data['Name']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            town = form.cleaned_data['town']
            address = Address.objects.get(Name=name, country=country, city=city, town=town)
            account.addresses.add(address)
            return redirect("home")
        else:
            messages.error(request, form.errors)
            form = AddressForm(None)
            data = {"form": form}
            return render(request, "add_address.html", data)

def makeComment(request, id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        name = request.POST["Name"]
        email = request.POST["Email"]
        text = request.POST["Text"]
        ProductComment.objects.create(product=product, Name=name, Email=email, Text=text)
        product.save()
        return redirect("productDetail", id=id)


############# Authentications ###############

class LoginView(View):

    def get(self, request):
        form = LoginForm(None)
        data = {"form": form}
        return render(request, "login.html", data)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "There is No Account")
                form = LoginForm(None)
                return render(request, "login.html", {"form": form})
        else:
            form = LoginForm(None)
            return render(request, "login.html", {"form": form})


def Logout(request):
    logout(request)
    return redirect("home")


def SelectRegisterType(request):
    return render(request, "select_register_type.html")


class CustomerRegisterView(View):

    def get(self, request):
        form = CustomerRegisterForm(None)
        data = {"form": form}
        return render(request, "register.html", data)

    def post(self, request):
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create(username=username, password=password)
            user.set_password(password)
            user.save()

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            lastName = form.cleaned_data['lastName']

            customerAccount = CustomerAccount.objects.create(user=user, Name=name, Email=email, LastName=lastName)
            customerAccount.save()

            shopCart = Order.objects.create(account=user)
            shopCart.save()

            authUser = authenticate(username=username, password=password)
            if authUser is not None:
                login(request, authUser)
                return redirect("home")
            else:
                messages.error(request, "ACcount Error")
                form = CustomerRegisterForm(None)
                data = {"form": form}
                return render(request, "register.html", data)

        else:
            errors = form.errors
            messages.error(request, errors)
            form = CustomerRegisterForm(None)
            data = {"form": form}
            return render(request, "register.html", data)


class ShopRegisterView(View):

    def get(self, request):
        form = ShopRegisterForm(None)
        data = {"form": form}
        return render(request, "register.html", data)

    def post(self, request):
        form = ShopRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create(username=username, password=password)
            user.set_password(password)
            user.save()

            shopName = form.cleaned_data['shopName']
            addres = form.cleaned_data['addres']
            email = form.cleaned_data['email']

            shop = ShopAccount.objects.create(user=user, ShopName=shopName, Addres=addres, Email=email)
            shop.save()

            shopCart = Order.objects.create(account=user)
            shopCart.save()

            authUser = authenticate(username=username, password=password)
            if authUser is not None:
                login(request, authUser)
                return redirect("home")
            else:
                messages.error(request, "ACcount Error")
                form = CustomerRegisterForm(None)
                data = {"form": form}
                return render(request, "register.html", data)

        else:
            errors = form.errors
            messages.error(request, errors)
            form = ShopRegisterForm(None)
            data = {"form": form}
            return render(request, "register.html", data)


# Product Operations
class NewProductView(View):

    def get(self, request):
        if request.user.is_authenticated:
            form = NewProductForm(None)
            data = {"form": form}
            return render(request, "new_product.html", data)
        else:
            return response.Http404()

    def post(self, request):
        if request.user.is_authenticated:
            form = NewProductForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data["Name"]
                price = form.cleaned_data["Price"]
                description = form.cleaned_data["Description"]
                category = form.cleaned_data["Category"]
                brand = form.cleaned_data["Brand"]

                photo1 = form.cleaned_data["Photo1"]
                photo2 = form.cleaned_data["Photo2"]
                photo3 = form.cleaned_data["Photo3"]
                photo4 = form.cleaned_data["Photo4"]
                photo5 = form.cleaned_data["Photo5"]

                shop = ShopAccount.objects.get(user=request.user)
                date = datetime.datetime.now()

                newProduct = Product.objects.create(
                    Name=name,
                    Price=price,
                    Description=description,
                    Category=category,
                    Brand=brand,
                    Photo1=photo1,
                    Photo2=photo2,
                    Photo3=photo3,
                    Photo4=photo4,
                    Photo5=photo5,
                    Shop=shop,
                    UploadDate=date
                )

                newProduct.save()

                return redirect("home")

            else:
                messages.error(request, form.errors)
                form = NewProductForm(None)
                data = {"form": form}
                return render(request, "new_product.html", data)
        else:
            return response(404)


def deleteOrderItem(request, id):
    orderItem = OrderItem.objects.get(id=id)
    order = Order.objects.get(account=request.user)
    orderItem.delete()
    order.save()
    return redirect(request.META.get('HTTP_REFERER'))


def shopCartView(request):
    cart = Order.objects.get(account=request.user)
    total = 0
    for item in cart.items.all():
        total += item.product.Price
    cart.totalPrice = total
    cart.save()
    account = findAccount(user=request.user)
    data = {"cart": cart, "account": account}
    if (request.user.is_authenticated):
        cart = get_object_or_404(Order, account=request.user)
        data['shopCart'] = cart
    return render(request, "shopCart.html", data)


def orderRequests(request):
    shop = ShopAccount.objects.get(user=request.user)
    requestedOrders = OrderItem.objects.filter(product__Shop=shop, isBuyed=True)
    confirmedOrders = OrderItem.objects.filter(product__Shop=shop, isConfirmed=True)
    sendedOrders = OrderItem.objects.filter(product__Shop=shop, isShipping=True)
    data = {"requestedOrders": requestedOrders, "confirmedOrders": confirmedOrders, "sendedOrders": sendedOrders}
    if (request.user.is_authenticated):
        cart = get_object_or_404(Order, account=request.user)
        total = 0
        for item in cart.items.all():
            total += item.product.Price
        cart.totalPrice = total
        cart.save()
        data['shopCart'] = cart
    return render(request, "order_requests.html", data)


def buyOrders(request):
    cart = Order.objects.get(account=request.user)
    for item in cart.items.all():
        item.isBuyed = True
        item.save()
        cart.items.remove(item)

    return redirect("home")


def cancelOrder(request, id):
    order = OrderItem.objects.get(id=id)
    order.delete()
    return redirect("purchasedOrders")


def purchasedOrders(request):
    purchased_orders = OrderItem.objects.filter(customer=request.user, isBuyed=True)
    confirmed_orders = OrderItem.objects.filter(customer=request.user, isConfirmed=True)
    shipping_orders = OrderItem.objects.filter(customer=request.user, isShipping=True)
    data = {"purchased_orders": purchased_orders, "confirmed_orders": confirmed_orders,
            "shipping_orders": shipping_orders}
    return render(request, "purchased_orders.html", data)


def refuseOrder(request, id):
    order = OrderItem.objects.get(id=id)
    order.delete()
    return redirect("orderRequests")


def confirmOrder(request, id):
    print("IDDDDDD", id)
    order = OrderItem.objects.get(id=id)
    order.isBuyed = False
    order.isConfirmed = True
    order.save()
    return redirect("orderRequests")


def sendOrder(request, id):
    cargoNumber = request.POST['cargoNumber']
    order = OrderItem.objects.get(id=id)
    order.cargoNumber = cargoNumber
    order.isConfirmed = False
    order.isShipping = True
    order.save()
    return redirect("orderRequests")


def finishOrder(request, id):
    order = OrderItem.objects.get(id=id)
    order.isShipping = False
    order.isFinished = True
    order.save()
    return redirect("purchasedOrders")
