from django.shortcuts import get_object_or_404
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
    CustomerGetOfferSerializer,
    CustomerPostOfferSerializer,
)
from applications.customers.models import Customers
from applications.customers.services import VerifyEmail, OfferService


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
        email = request.query_params.get("email")
        token = request.query_params.get("token")
        customer = get_object_or_404(Customers, email=email)

        serializer = self.get_serializer(data={"token": token})
        if serializer.is_valid():
            customer.is_confirmed_email = True
            customer.save()

        return Response(
            {"message": "Email has been verified"}, status=status.HTTP_200_OK
        )


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


class CustomerOfferView(generics.CreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerGetOfferSerializer

    def create(self, request, *args, **kwargs):
        offer = OfferService(request).form_offer()

        serializer = CustomerPostOfferSerializer(data=offer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
