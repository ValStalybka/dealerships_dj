from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.dealerships import views

router = DefaultRouter()
router.register(r"dealerships", views.DealershipViewSet, basename="dealerships")
router.register(r"cars", views.CarsViewSet, basename="cars")

urlpatterns = [
    path("", include((router.urls, "dealerships"))),
    path(
        "dealerships/<int:pk>/order/",
        views.DealershipOrderView.as_view(),
        name="dealerships-order",
    ),
    path(
        "dealerships/<int:pk>/stats/",
        views.DealershipStatisticsView.as_view(),
        name="dealerships-stats",
    ),
    path(
        "dealerships/<int:pk>/discounts/",
        views.DealershipDiscountView.as_view(),
        name="dealerships-discounts",
    ),
]
