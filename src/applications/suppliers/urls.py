from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.suppliers import views

router = DefaultRouter()
router.register(r"suppliers", views.SupplierViewSet, basename="suppliers")

urlpatterns = [
    path("", include((router.urls, "suppliers"))),
    path(
        "suppliers/<int:pk>/discounts/",
        views.SupplierDiscountView.as_view(),
        name="supplier-discounts",
    ),
]
