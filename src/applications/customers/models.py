from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from rest_framework_simplejwt.tokens import RefreshToken

from applications.core import CommonInfo
from applications.customers.managers import CustomerManager


class Customers(AbstractUser, CommonInfo):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    balance = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", default=0
    )
    offer = models.JSONField(blank=True, null=True, default=None)
    is_confirmed_email = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class Profiles(CommonInfo):
    customer_id = models.OneToOneField(Customers, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400)
    birthday = models.DateField()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
