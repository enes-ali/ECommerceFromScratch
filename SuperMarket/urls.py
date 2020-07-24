from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeView, name="home"),
    path("product/<int:id>", DetailView.as_view(), name="productDetail"),
    path("addAddress", addAddressView.as_view(), name="addAddress"),
    path("makeComment/<int:id>", makeComment, name="makeComment"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", Logout, name="logout"),
    path("newProduct", NewProductView.as_view(), name="newProduct"),
    path("selectRegister", SelectRegisterType, name="selectRegister"),
    path("registerCustomer", CustomerRegisterView.as_view(), name="customerRegister"),
    path("registerShop", ShopRegisterView.as_view(), name="shopRegister"),
    path("deleteOrderItem/<int:id>", deleteOrderItem, name="deleteOrderItem"),
    path("shopCart", shopCartView, name="shopCart"),
    path("orderRequests", orderRequests, name="orderRequests"),
    path("buyOrders", buyOrders, name="buyOrders"),
    path("cancelOrder/<int:id>", cancelOrder, name="cancelOrder"),
    path("purchasedOrders", purchasedOrders, name="purchasedOrders"),
    path("refuseOrder/<int:id>", refuseOrder, name="refuseOrder"),
    path("confirmOrder/<int:id>", confirmOrder, name="confirmOrder"),
    path("sendOrder/<int:id>", sendOrder, name="sendOrder"),
    path("finishOrder/<int:id>", finishOrder, name="finishOrder"),
]
