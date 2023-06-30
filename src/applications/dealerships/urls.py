from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"dealerships", views.DealershipViewSet, basename="dealerships")
router.register(r"cars", views.CarsViewSet, basename="cars")

urlpatterns = [
    path("", include((router.urls, "dealerships"))),
    path("dealerships/<int:pk>/order/", views.DealershipOrderView.as_view()),
]
