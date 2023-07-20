from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from applications.customers.models import Customers, Profiles
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = PasswordField()

    class Meta:
        model = Customers
        fields = ["first_name", "last_name", "balance", "email", "password"]

    def validate(self, attrs):
        try:
            validate_password(attrs["password"])
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})

        return attrs

    def create(self, validated_data):
        return Customers.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = PasswordField()

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_confirmed_email:
            raise serializers.ValidationError(
                "Email has not been verified, check your inbox"
            )
        return user.tokens


class ChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField()
    new_password = PasswordField()
    new_password2 = PasswordField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": "Password doesn't match"}
            )

        try:
            validate_password(attrs["new_password"])
        except ValidationError as err:
            raise serializers.ValidationError({"new_password": err.messages})
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    customer_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profiles
        fields = ["customer_id", "bio", "birthday"]
