from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q, F
from django.db.models.functions import Now
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from applications.core import CommonInfo


class AbstractDiscount(CommonInfo):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cars = models.JSONField()
    percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])

    class Meta:
        abstract = True
        ordering = ["created_at"]


class AbstractSale(CommonInfo):
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")

    class Meta:
        abstract = True


class Cars(CommonInfo):
    class TransmissionType(models.TextChoices):
        MANUAL = "MN", "Manual"
        AUTOMATIC = "AU", "Automatic"

    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(validators=[MaxValueValidator(2023)])
    color = models.CharField(max_length=25)
    fuel_type = models.CharField(max_length=25)
    transmission = models.CharField(
        choices=TransmissionType.choices, default=TransmissionType.MANUAL
    )
    is_discounted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-year", "brand"]

    def __str__(self):
        return f"{self.brand} {self.model}"


class Dealerships(CommonInfo):
    name = models.CharField(max_length=50)
    location = CountryField()
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    cars = models.ManyToManyField(
        Cars, through="DealershipCars", related_name="dealerships"
    )
    customers = models.ManyToManyField("customers.Customers", through="DealershipSales")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DealershipCars(CommonInfo):
    dealership_id = models.ForeignKey(Dealerships, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    amount = models.PositiveIntegerField()


class DealershipSales(AbstractSale):
    customer_id = models.ForeignKey(
        "customers.Customers", on_delete=models.CASCADE, related_name="bought"
    )
    dealership_id = models.ForeignKey(
        Dealerships, on_delete=models.CASCADE, related_name="sold"
    )


class DealershipsDiscounts(AbstractDiscount):
    dealership = models.ForeignKey(
        Dealerships, on_delete=models.CASCADE, related_name="discounts"
    )
