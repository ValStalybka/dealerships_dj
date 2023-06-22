from django.core.validators import MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField


class CommonInfo(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
