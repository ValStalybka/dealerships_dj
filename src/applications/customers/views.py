from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from applications.customers.permissions import IsOwnerOrReadOnly
from applications.customers.serializers import (
    RegisterSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
)
from applications.customers.models import Customers
from applications.customers.services import VerifyEmail


class CustomerRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        data["tokens"] = user.tokens
        VerifyEmail(request, data).send_verification_email()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerificationView(generics.GenericAPIView):
    queryset = Customers.objects.all()
    serializer_class = TokenVerifySerializer

    def get(self, request):
        pass


class CustomerLoginView(generics.GenericAPIView):
    queryset = Customers.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Customers.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)


class ProfileCreateView(generics.CreateAPIView):
    queryset = Customers.objects.select_related("profile").all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
