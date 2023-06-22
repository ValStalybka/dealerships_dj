from django.contrib import admin
from .models import Customers, Profiles


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "email", "balance"]
    list_display = ["first_name", "last_name", "email", "balance"]
    ordering = ("last_name", "created_at")
    search_fields = ("first_name", "last_name")


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    fields = ["customer_id", "bio", "birthday"]
    list_display = ["customer_id", "bio", "birthday", "created_at"]
    ordering = ("customer_id",)
    search_fields = ("customer_id", )