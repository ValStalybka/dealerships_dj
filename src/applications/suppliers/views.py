from rest_framework import mixins, filters, generics
from rest_framework.viewsets import GenericViewSet
from applications.suppliers.serializers import (
    SupplierSerializer,
    SupplierDiscountSerializer,
)
from applications.suppliers.models import Suppliers, SupplierDiscounts


class SupplierViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Suppliers.objects.prefetch_related("cars")
    serializer_class = SupplierSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("year_founded",)


class SupplierDiscountView(generics.ListCreateAPIView):
    queryset = SupplierDiscounts
    serializer_class = SupplierDiscountSerializer
