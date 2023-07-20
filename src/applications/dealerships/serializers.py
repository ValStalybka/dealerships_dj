from rest_framework import serializers

from applications.dealerships.models import (
    Dealerships,
    Cars,
    DealershipCars,
    DealershipDiscounts,
)
from applications.suppliers.models import SupplierCars


class DealershipSerializer(serializers.ModelSerializer):
    cars = serializers.StringRelatedField(many=True)

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


class DealershipCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCars
        fields = ["dealership", "car", "price", "amount"]


class CarDiscountSerializer(serializers.Serializer):
    car_list = serializers.PrimaryKeyRelatedField(
        queryset=Cars.objects.all(), many=True
    )

    def to_representation(self, instance):
        instance = {
            "car_list": [Cars.objects.get(pk=pk) for pk in instance["car_list"]]
        }
        representation = super().to_representation(instance)
        return representation


class DealershipDiscountSerializer(serializers.Serializer):
    dealership = serializers.PrimaryKeyRelatedField(queryset=Dealerships.objects.all())
    name = serializers.CharField()
    description = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    cars = CarDiscountSerializer()
    percent = serializers.IntegerField()

    def create(self, validated_data):
        return DealershipDiscounts.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

    def to_internal_value(self, data):
        data1 = super().to_internal_value(data)
        data1["cars"] = {"car_list": [obj.pk for obj in data1["cars"]["car_list"]]}
        return data1
