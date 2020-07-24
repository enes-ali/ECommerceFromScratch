from .models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        url = "http://192.168.1.105:8000"
        data = super().to_representation(instance)
        data["Photo1"] = url + data["Photo1"][6:]
        data["Photo2"] = url + data["Photo2"][6:]
        data["Photo3"] = url + data["Photo3"][6:]
        data["Photo4"] = url + data["Photo4"][6:]
        data["Photo5"] = url + data["Photo5"][6:]
        print(data["Photo2"])
        return data
