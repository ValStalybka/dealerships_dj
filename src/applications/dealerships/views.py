from rest_framework import mixins, generics, filters, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from applications.dealerships.serializers import (
    DealershipSerializer,
    CarSerializer,
    DealershipGetOrderSerializer,
    DealershipPostOrderSerializer,
    DealershipCarsSerializer,
    DealershipDiscountSerializer,
)
from applications.dealerships.models import (
    Dealerships,
    Cars,
    DealershipCars,
    DealershipDiscounts,
)
from applications.dealerships.services import (
    FormOrderService,
    DealershipStatisticsService,
    change_car_price,
)


class DealershipViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Dealerships.objects.prefetch_related("cars")
    serializer_class = DealershipSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("location",)


class CarsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer


class DealershipOrderView(generics.CreateAPIView):
    queryset = Dealerships.objects.all()
    serializer_class = DealershipGetOrderSerializer

    def create(self, request, *args, **kwargs):
        order = FormOrderService(kwargs.get("pk"), request).form_order()

        # checking if any errors occurred while forming order
        if isinstance(order, Response):
            return order

        # creating instance in SupplierCars model
        supplier_serializer = DealershipPostOrderSerializer(data=order)
        supplier_serializer.is_valid(raise_exception=True)
        self.perform_create(supplier_serializer)

        # creating instance in DealershipCars model
        dealership_serializer = DealershipCarsSerializer(data=change_car_price(order))
        dealership_serializer.is_valid(raise_exception=True)
        dealership_serializer.save()

        headers = self.get_success_headers(supplier_serializer.data)
        return Response(
            supplier_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class DealershipStatisticsView(generics.RetrieveAPIView):
    queryset = DealershipCars.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = DealershipStatisticsService(pk=kwargs.get("pk")).get_statistic()
        return Response(instance)


class DealershipDiscountView(generics.ListCreateAPIView):
    queryset = DealershipDiscounts.objects.all()
    serializer_class = DealershipDiscountSerializer

    # def list(self, request, *args, **kwargs):
    #     discounts = DealershipDiscounts.objects.all()
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
