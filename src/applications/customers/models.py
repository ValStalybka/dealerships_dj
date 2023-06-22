from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from djmoney.models.fields import MoneyField

from applications.core import CommonInfo


class Customers(AbstractBaseUser, CommonInfo):
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    offer = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Profiles(CommonInfo):
    customer_id = models.OneToOneField(Customers, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400)
    birthday = models.DateField()
