# Generated by Django 4.2.2 on 2023-06-27 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0001_initial"),
        ("dealerships", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dealershipcars",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bought",
                to="customers.customers",
            ),
        ),
    ]
