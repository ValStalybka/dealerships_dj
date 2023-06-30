from rest_framework import status
from rest_framework.response import Response
from collections import namedtuple
from django.shortcuts import get_object_or_404
from typing import NamedTuple
from decimal import Decimal
from applications.dealerships.models import Dealerships
from applications.suppliers.models import SupplierCars


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

    def _check_for_discounts_from_supplier(self, order_info: NamedTuple):
        """checks for discounts from supplier"""
        pass

    def _find_total_order_sum(self) -> Decimal:
        """calculates final sum of money
        buyer has to spend on the order"""
        price = self._find_best_offer_for_car().price
        if self._error_response:
            return self._error_response

        return Decimal(self.amount) * price

    def _check_is_enough_money(self) -> None:
        """checks if dealership has enough money
        to make a purchase"""
        if self._error_response:
            return self._error_response

        dealership = get_object_or_404(Dealerships, pk=self.pk)
        if self._find_total_order_sum() > dealership.balance.amount:
            self._error_response = Response(
                data={"error": "Not enough money to make a purchase"}
            )
            return self._error_response

    def make_purchase(self) -> None:
        """updates dealership's balance
        according to purchase sum"""
        dealership = Dealerships.objects.get(pk=self.pk)
        print(self._find_total_order_sum())
        dealership.balance.amount = (
            dealership.balance.amount - self._find_total_order_sum()
        )
        dealership.save()

    def form_order(self) -> dict:
        """returns finished order from a dealership"""
        offer = self._find_best_offer_for_car()
        self._check_is_enough_money()
        if self._error_response:
            return self._error_response
        return {
            "supplier": offer.supplier,
            "car": self.car,
            "price": offer.price,
            "amount": int(self.amount),
            "dealership": self.pk,
        }
