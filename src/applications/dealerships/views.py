from rest_framework import mixins, generics, filters, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    DealershipSerializer,
    CarSerializer,
    DealershipGetOrderSerializer,
    DealershipPostOrderSerializer,
)
from .models import Dealerships, Cars
from .services import FormOrderService


class DealershipViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Dealerships.objects.all()
    serializer_class = DealershipSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = [
        "location",
    ]


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
        order = FormOrderService(kwargs.get("pk"), request)

        """checking if any errors occurred while forming order"""
        if isinstance(order.form_order(), Response):
            return order.form_order()

        serializer = DealershipPostOrderSerializer(data=order.form_order())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        order.make_purchase()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
