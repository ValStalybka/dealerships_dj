import pytest
from rest_framework.test import APIClient

from applications.dealerships.models import Dealerships, Cars
from applications.suppliers.models import Suppliers, SupplierCars


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def create_dealership():
    dealership = {
        "name": "test dealership",
        "location": "NZ",
        "balance": 12000,
    }
    instance = Dealerships.objects.create(**dealership)
    return instance


@pytest.fixture()
def create_car():
    car = {
        "brand": "Volkswagen",
        "model": "Polo",
        "year": 2010,
        "color": "BK",
        "fuel_type": "Gasoline",
        "transmission": "AU",
    }

    instance = Cars.objects.create(**car)
    return instance


@pytest.fixture()
def create_supplier():
    supplier = {
        "name": "test supplier",
        "year_founded": 2010,
    }
    instance = Suppliers.objects.create(**supplier)
    return instance


@pytest.fixture()
def create_supplier_car(create_car, create_supplier):
    supplier_car = {"supplier": create_supplier, "car": create_car, "price": 2000}
    instance = SupplierCars.objects.create(**supplier_car)
    return instance
