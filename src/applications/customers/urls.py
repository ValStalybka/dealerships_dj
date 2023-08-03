from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from applications.customers import views


urlpatterns = [
    path("register/", views.CustomerRegisterView.as_view(), name="sign_up"),
    path("login/", views.CustomerLoginView.as_view(), name="log_in"),
    path("email-verify/", views.EmailVerificationView.as_view(), name="email-verify"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(
        "<int:pk>/change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "customer/<int:pk>/profile",
        views.ProfileCreateView.as_view(),
        name="profile-list",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("customer/<int:pk>/offer", views.CustomerOfferView.as_view(), name="offer"),
]
