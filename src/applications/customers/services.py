from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Min, Sum
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from applications.core import error_handler
from applications.customers.models import Customers
from applications.dealerships.models import (
    DealershipCars,
    DealershipDiscounts,
    Dealerships,
)


class VerifyEmail:
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def _get_verification_url(self) -> str:
        """returns email confirmation url
        based on Customer's token"""
        current_site = get_current_site(self.request).domain
        endpoint = reverse("email-verify")
        access_token = self.data["tokens"]["access"]
        email = self.data["email"]
        absolute_url = (
            f"https://{current_site}{endpoint}?email={email}&token={access_token}"
        )
        return absolute_url

    def send_verification_email(self) -> None:
        """sends an email to Customer's inbox
        in order to verify an account"""
        email = EmailMessage(
            subject="Email verification",
            body=f"Please, verify your email \n{self._get_verification_url()}",
            to=(self.data["email"],),
        )

        email.send()


class OfferService:
    __error_response = None

    def __init__(self, request):
        self.car = request.data["car"]
        self.price = request.data["price"]
        self.customer = Customers.objects.get(id=request.data["customer"])

    @property
    def _error_response(self):
        return self.__error_response

    @_error_response.setter
    def _error_response(self, value):
        self.__error_response = value

    @error_handler
    def _check_discounts(self):
        """checks if Dealership has discounts for specific car"""
        subquery = (
            DealershipDiscounts.objects.exclude(end_date__lte=timezone.now()).filter(
                cars__car_list__contains=int(self.car)
            )
        ).values("dealership", "percent")
        return subquery

    @error_handler
    def _find_best_offer(self):
        """finds an offer from dealership with minimal price"""
        cars = (
            DealershipCars.objects.filter(car=self.car)
            .values("dealership")
            .annotate(total_amount=Sum("amount"))
            .filter(customer=None, price__lte=self.price)
            .annotate(min_price=Min("price"))
            .order_by("price")
        )

        try:
            car = cars[0]

        except IndexError:
            self._error_response = Response(
                data={"error": "No offers found"},
                status=status.HTTP_404_NOT_FOUND,
            )
            return self._error_response
        return car

    @error_handler
    def _make_purchase(self, customer, dealership, price) -> None:
        """updates Dealership's balance and Customer's balance"""
        dealership.balance.amount = dealership.balance.amount + price
        customer.balance.amount = customer.balance.amount - price
        dealership.save()

    def form_offer(self) -> dict:
        """returns finished order from a customer"""

        offer = self._find_best_offer()
        dealership = Dealerships.objects.get(id=offer["dealership"])
        if self._error_response:
            return self._error_response
        self._make_purchase(self.customer, dealership, offer["min_price"])
        return {
            "dealership": offer["dealership"],
            "car": self.car,
            "customer": self.customer.id,
            "price": offer["min_price"],
            "amount": -1,
        }
