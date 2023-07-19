from rest_framework import status
from rest_framework.response import Response
from collections import namedtuple
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, F
from typing import NamedTuple
from decimal import Decimal

from applications.dealerships.models import Dealerships, DealershipCars
from applications.suppliers.models import SupplierCars, SupplierDiscounts
from applications.core import error_handler


class FormOrderService:
    """class for forming an order from dealerships"""

    __error_response = None

    def __init__(self, pk: int, request):
        self.car = request.data["car"]
        self.amount = request.data["amount"]
        self.pk = pk

    @property
    def _error_response(self):
        return self.__error_response

    @_error_response.setter
    def _error_response(self, value):
        self.__error_response = value

    def _find_best_offer_for_car(self) -> NamedTuple:
        """compares price for car instance from different suppliers"""
        cars = SupplierCars.objects.filter(car=self.car, dealership=None).order_by(
            "price"
        )

        try:
            best_offer = cars[0]

        except IndexError:
            self._error_response = Response(
                data={"error": "Suppliers don't have this car right now"},
                status=status.HTTP_404_NOT_FOUND,
            )
            return self._error_response
        Order_info = namedtuple("Order_info", "supplier price")
        order_info = Order_info(best_offer.supplier.id, best_offer.price.amount)

        return order_info

    def _check_for_discounts_from_supplier(self, cars):
        """checks for discounts from supplier"""
        SupplierDiscounts.objects.filter(cars__cars__contains=[self.car]).annotate(
            new_price=F("percent") * F("suppliercars__price")
        )
        pass

    @error_handler
    def _find_total_order_sum(self, offer: NamedTuple) -> Decimal:
        """calculates final sum of money
        buyer has to spend on the order"""
        return Decimal(self.amount) * offer.price

    @error_handler
    def _is_enough_money(self, total_sum: Decimal, dealership: Dealerships) -> bool:
        """checks if dealership has enough money
        to make a purchase"""
        if total_sum > dealership.balance.amount:
            return False

        return True

    @error_handler
    def _make_purchase(self, total_sum: Decimal, dealership: Dealerships) -> None:
        """updates dealership's balance
        according to purchase sum"""
        dealership.balance.amount = dealership.balance.amount - total_sum
        dealership.save()

    def form_order(self) -> dict:
        """returns finished order from a dealership"""
        dealership = get_object_or_404(Dealerships, pk=self.pk)
        offer = self._find_best_offer_for_car()
        total_sum = self._find_total_order_sum(offer=offer)

        if not self._is_enough_money(total_sum, dealership):
            self._error_response = Response(
                data={"error": "Not enough money to make a purchase"}
            )
            return self._error_response

        if self._error_response:
            return self._error_response

        self._make_purchase(total_sum, dealership)
        return {
            "supplier": offer.supplier,
            "car": self.car,
            "price": offer.price,
            "amount": int(self.amount),
            "dealership": self.pk,
        }


def change_car_price(data: dict) -> dict:
    """raises car's price by 15% so a dealership can make profit"""
    data["price"] = (data["price"] * Decimal(1.15)).quantize(Decimal("1.00"))
    return data


class DealershipStatisticsService:
    """class for aggregating statistic for Dealership instance"""

    def __init__(self, pk):
        self.pk = pk

    def get_statistic(self):
        """returns statistic for a specific dealership,such as
        gross income, unique customers and number of cars sold"""
        return (
            DealershipCars.objects.exclude(customer=None)
            .filter(dealership_id=self.pk)
            .aggregate(
                unique_customers=Count("customer", distinct=True),
                cars_sold=Count("id", distinct=True),
                income=Sum("price"),
            )
        )
