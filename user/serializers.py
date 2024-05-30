from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from user.helpers import send_reset_password_email

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password_2",
            "avatar",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_2")

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if user := authenticate(email=email, password=password):
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("Your Email or password is incorrect.")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_2"]:
            raise serializers.ValidationError(
                {"new_password": "New password fields didn't match."}
            )

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        return value

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        send_reset_password_email(user=user)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    new_password_2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_2"]:
            raise serializers.ValidationError("Password fields didn't match.")

        try:
            uid = force_str(urlsafe_base64_decode(self.context.get("uid")))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID")
        if not default_token_generator.check_token(user, self.context.get("token")):
            raise serializers.ValidationError("Invalid token or user ID")

        return attrs

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.context.get("uid")))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data["new_password"])
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "avatar"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        if "avatar" in validated_data:
            instance.avatar = validated_data["avatar"]

        instance.save()

        return instance
