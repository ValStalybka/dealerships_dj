from django.contrib import admin
from applications.suppliers.models import Suppliers, SupplierCars, SupplierDiscounts


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    fields = ["name", "year_founded"]
    list_display = ["name", "year_founded", "created_at"]
    ordering = ("name", "year_founded", "created_at")
    search_fields = ("name",)


@admin.register(SupplierCars)
class SupplierCarsAdmin(admin.ModelAdmin):
    fields = ["supplier", "dealership", "car", "price", "amount"]
    list_display = ["supplier", "dealership", "car", "price", "amount", "created_at"]
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
