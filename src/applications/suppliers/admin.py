from django.contrib import admin
from .models import Suppliers, SupplierCars, SupplierDiscounts


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    fields = ["name", "year_founded"]
    list_display = ["name", "year_founded", "created_at"]
    ordering = ("name", "year_founded", "created_at")
    search_fields = ("name",)


@admin.register(SupplierCars)
class SupplierCarsAdmin(admin.ModelAdmin):
    fields = ["supplier", "dealership", "car", "price"]
    list_display = ["supplier", "dealership", "car", "price", "created_at"]
    ordering = ("supplier", "dealership", "created_at")
    search_fields = (
        "supplier",
        "dealership",
    )


@admin.register(SupplierDiscounts)
class SupplierDiscountsCarsAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "description",
        "supplier",
        "start_date",
        "end_date",
        "cars",
        "percent",
    ]
    list_display = [
        "name",
        "description",
        "supplier",
        "start_date",
        "end_date",
        "cars",
        "percent",
    ]
    ordering = ("supplier", "start_date", "percent")
    search_fields = ("supplier", "name")
