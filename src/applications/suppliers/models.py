from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField

from applications.core import CommonInfo, AbstractDiscount


class Suppliers(CommonInfo):
    name = models.CharField(max_length=50)
    year_founded = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2023)]
    )
    cars = models.ManyToManyField(
        "dealerships.Cars", through="SupplierCars", related_name="suppliers"
    )

    class Meta:
        ordering = ["name", "year_founded"]

    def __str__(self):
        return self.name


class SupplierCars(CommonInfo):
    supplier = models.ForeignKey(
        Suppliers, on_delete=models.CASCADE, related_name="sold"
    )
    car = models.ForeignKey("dealerships.Cars", on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    dealership = models.ForeignKey(
        "dealerships.Dealerships", on_delete=models.CASCADE, related_name="bought"
    )


class SupplierDiscounts(AbstractDiscount):
    supplier = models.ForeignKey(
        Suppliers, on_delete=models.CASCADE, related_name="discounts"
    )
