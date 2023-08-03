from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from decimal import Decimal

from applications.dealerships.models import DealershipCars, Cars, Dealerships
from applications.suppliers.models import Suppliers, SupplierCars

logger = get_task_logger(__name__)


def get_best_supplier(car: Cars) -> Suppliers:
    """takes a Cars instanse and returns Suppliers
    instance with best price for that car"""

    supplier_cars = SupplierCars.objects.filter(car=car).order_by("price").first()
    return supplier_cars


def is_enough_money(dealership: Dealerships, total_sum: Decimal) -> bool:
    """checks if dealership has enough money to make a purchase"""
    return dealership.balance.amount >= total_sum


def find_total_order_sum(amount: int, price: Decimal) -> Decimal:
    """calculates total order sum based on price and amount"""
    return Decimal(amount) * price


def make_money_transaction(dealership: Dealerships, total_sum: Decimal) -> None:
    dealership.balance.amount -= total_sum
    dealership.save()


@shared_task()
def make_purchase():
    dealer_cars = DealershipCars.objects.filter(customer=None).distinct(
        "dealership", "car"
    )
    amount = 6

    for dealer_car in dealer_cars:
        dealership = dealer_car.dealership
        car = dealer_car.car
        supplier_offer = get_best_supplier(car)

        try:
            price = supplier_offer.price.amount
            total_sum = find_total_order_sum(amount, price)
            enough_money = is_enough_money(dealership, total_sum)

        except AttributeError:
            logger.info(f"No supplier has {car} right now")

        if supplier_offer and enough_money:
            print(dealership, car)
            make_money_transaction(supplier_offer.supplier, dealership, total_sum)

            SupplierCars.objects.create(
                dealership=dealership,
                car=car,
                supplier=supplier_offer.supplier,
                price=price,
                amount=amount,
            )
            DealershipCars.objects.create(
                dealership=dealership,
                car=car,
                customer=None,
                price=price,
                amount=amount,
            )
