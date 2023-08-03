import pytest
from rest_framework import status
from django.urls import reverse
from applications.dealerships.models import Dealerships


@pytest.mark.django_db
def test_order(api_client, create_dealership, create_supplier_car):
    url = reverse("dealerships-order", kwargs={"pk": create_dealership.id})
    data = {
        "supplier": create_supplier_car.supplier.id,
        "dealership": create_dealership.id,
        "price": create_supplier_car.price.amount,
        "car": create_supplier_car.car.id,
        "amount": 2,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    "name, location, balance",
    [("dealership 1", "BY", 0), ("dealership 2", "NZ", 10000)],
)
@pytest.mark.django_db
def test_created_dealership(name, location, balance):
    Dealerships.objects.create(name=name, location=location, balance=balance)
    assert Dealerships.objects.filter(name=name).exists() is True


@pytest.mark.django_db
def test_connection(api_client):
    response = api_client.get(reverse("dealerships:dealerships-list"))
    assert response.status_code == status.HTTP_200_OK
