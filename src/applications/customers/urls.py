from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from applications.customers import views


urlpatterns = [
    path("register/", views.CustomerRegisterView.as_view(), name="sign_up"),
    path("login/", views.CustomerLoginView.as_view(), name="log_in"),
    path("email-verify/", views.EmailVerificationView.as_view(), name="email-verify"),
    path(
        "<int:pk>/change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("profile/<int:pk>/", views.ProfileCreateView.as_view(), name="profile-list"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
