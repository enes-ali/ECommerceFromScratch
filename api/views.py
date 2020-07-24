from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response


class AllProducts(APIView):

    def get(self, request):
        products = Product.objects.all()
        print(products[4].Photo1)
        jsons = ProductSerializer(products, many=True)
        print(jsons.data[4]["Photo1"])
        return Response(jsons.data)

    
class getProduct(APIView):

    def get_object(self, id):
        product = get_object_or_404(Product, id=id)
        return product

    def get(self, request, id):
        product = self.get_object(id)
        json = ProductSerializer(product)
        return Response(json.data)