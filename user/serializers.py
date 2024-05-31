from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from user.helpers import send_reset_password_email

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the validation and creation of a new user,
    including password confirmation.
    """
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
        """
        Validate that the two password fields match.

        Raises a ValidationError if the passwords do not match.
        """
        if attrs["password"] != attrs["password_2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        Removes the password confirmation field before creating the user.
        """
        validated_data.pop("password_2")

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer handles the validation of user credentials and
    authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate user credentials.

        Authenticates the user with the provided email and password.
        If authentication is successful, adds the user to the validated
        data. Raises a ValidationError if authentication fails.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if user := authenticate(email=email, password=password):
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("Your Email or password is incorrect.")


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.

    This serializer handles the validation and updating of the user's
    password, including checking the old password and confirming the
    new password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """
        Validate the old password.

        Checks if the old password provided by the user is correct.
        Raises a ValidationError if the old password is incorrect.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")

        return value

    def validate(self, attrs):
        """
        Validate the new passwords.

        Ensures that the new password and confirmation password match.
        Raises a ValidationError if the passwords do not match.
        """
        if attrs["new_password"] != attrs["new_password_2"]:
            raise serializers.ValidationError(
                {"new_password": "New password fields didn't match."}
            )

        return attrs

    def save(self, **kwargs):
        """
        Save the new password.

        Updates the user's password with the new password and saves the user.
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for initiating a password reset.

    This serializer handles the validation of the user's email and
    triggers the password reset process.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate the email.

        Checks if a user with the provided email exists. Raises a
        ValidationError if no such user is found.
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        return value

    def save(self):
        """
        Trigger the password reset process.

        Sends a reset password email to the user with the provided email.
        """
        user = User.objects.get(email=self.validated_data["email"])
        send_reset_password_email(user=user)


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.

    This serializer handles the validation of the new passwords and
    verifies the password reset token and user ID.
    """
    new_password = serializers.CharField(write_only=True)
    new_password_2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate the new passwords and token.

        Ensures that the new password and confirmation password match.
        Verifies the password reset token and user ID. Raises a
        ValidationError if the passwords do not match or if the token
        or user ID is invalid.
        """
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
        """
        Save the new password.

        Sets the new password for the user and saves the user.
        """
        uid = force_str(urlsafe_base64_decode(self.context.get("uid")))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data["new_password"])
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user profile.

    This serializer handles the serialization and deserialization of
    user profile data, as well as updating the user profile.
    """

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "avatar"]

    def update(self, instance, validated_data):
        """
        Update the user profile.

        Updates the username, email, and avatar fields of the user
        instance with the validated data.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        if "avatar" in validated_data:
            instance.avatar = validated_data["avatar"]

        instance.save()

        return instance
