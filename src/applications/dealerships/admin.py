from django.contrib import admin
from .models import Cars, Dealerships, DealershipCars, DealershipDiscounts


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    fields = ["brand", "model", "year", "color", "fuel_type", "transmission", "is_discounted"]
    list_display = ["brand", "model", "year", "color", "fuel_type", "transmission", "is_discounted", "created_at"]
    ordering = ("brand", "model", "year", "created_at")
    search_fields = ("brand", "model", "year", "color", "fuel_type", "transmission")


@admin.register(Dealerships)
class DealershipsAdmin(admin.ModelAdmin):
    fields = ["name", "location", "balance", "cars"]
    list_display = ["name", "location", "balance", "cars", "created_at"]
    ordering = ("name", "location", "created_at")
    search_fields = ("name", "location")


@admin.register(DealershipCars)
class DealershipCarsAdmin(admin.ModelAdmin):
    fields = ["dealership_id", "car_id", "price", "amount", "customer"]
    list_display = ["dealership_id", "car_id", "price", "amount", "customer"]
    ordering = ("dealership_id", "car_id")
    search_fields = ("dealership_id", "car_id", "customer")


@admin.register(DealershipDiscounts)
class DealershipDiscountsCarsAdmin(admin.ModelAdmin):
    fields = ["name", "description", "dealership", "start_date", "end_date", "cars", "percent"]
    list_display = ["name", "description", "dealership", "start_date", "end_date", "cars", "percent"]
    ordering = ("dealership", "start_date", "percent")
    search_fields = ("dealership", "name")