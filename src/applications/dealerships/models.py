from django.core.validators import MaxValueValidator
from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from applications.core import CommonInfo, AbstractDiscount


class Cars(CommonInfo):
    class TransmissionType(models.TextChoices):
        MANUAL = "MN", "Manual"
        AUTOMATIC = "AU", "Automatic"

    class ColorChoices(models.TextChoices):
        BLACK = "BK", "Black"
        WHITE = "WH", "White"
        RED = "RD", "Red"
        YELLOW = "YL", "Yellow"
        GREY = "GR", "Grey"
        BLUE = "BL", "Blue"
        GREEN = "GN", "Green"

    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(validators=[MaxValueValidator(2023)])
    color = models.CharField(
        max_length=25, choices=ColorChoices.choices, default=ColorChoices.BLACK
    )
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

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DealershipCars(CommonInfo):
    dealership_id = models.ForeignKey(
        Dealerships, on_delete=models.CASCADE, related_name="sold"
    )
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="USD")
    amount = models.PositiveIntegerField()
    customer = models.ManyToManyField(
        "customers.Customers", related_name="bought", null=True, blank=True
    )


class DealershipDiscounts(AbstractDiscount):
    dealership = models.ForeignKey(
        Dealerships, on_delete=models.CASCADE, related_name="discounts"
    )
