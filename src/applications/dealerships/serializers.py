from rest_framework import serializers

from .models import Dealerships, Cars
from applications.suppliers.models import SupplierCars


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealerships
        fields = ["name", "location", "balance", "cars"]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ["brand", "model", "year", "color", "fuel_type", "transmission"]


class DealershipGetOrderSerializer(serializers.Serializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Cars.objects.all())
    amount = serializers.IntegerField()


class DealershipPostOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCars
        fields = ["supplier", "car", "price", "amount", "dealership"]
