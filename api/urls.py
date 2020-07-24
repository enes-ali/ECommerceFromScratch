from django.urls import path
from .views import *

urlpatterns = [
    path("AllProducts", AllProducts.as_view()),
    path("product/<int:id>", getProduct.as_view()),
]