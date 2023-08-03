from rest_framework import serializers
from applications.suppliers.models import Suppliers


class SupplierSerializer(serializers.ModelSerializer):
    cars = serializers.StringRelatedField(many=True)

    class Meta:
        model = Suppliers
        fields = ["name", "year_founded", "cars"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["cars"] = set(representation["cars"])
        return representation


class SupplierDiscountSerializer(serializers.Serializer):
    pass
