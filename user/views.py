from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    UserProfileSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.

    This view uses the UserRegisterSerializer to handle the registration
    of new users. It allows any user (including unauthenticated ones) to
    access this view.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class LoginView(ObtainAuthToken):
    """
    API view for user login.

    This view uses the LoginSerializer to validate user credentials and
    obtain an authentication token. Upon successful authentication, it
    returns a token that can be used for authenticated requests.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to authenticate a user and return an auth token.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API view for user logout.

    This view logs out the authenticated user by deleting their
    authentication token and calling the Django logout function.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to log out the user.

        This method deletes the user's authentication token and logs them out.
        """
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "You successfully logged out"},
            status=status.HTTP_200_OK
        )


class UserChangePasswordView(generics.UpdateAPIView):
    """
    API view for changing the user's password.

    This view allows authenticated users to change their password using
    the ChangePasswordSerializer. The view ensures that the user can
    only change their own password.
    """
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """
        Retrieve and return the authenticated user.

        This method is used to ensure that the password change operation
        applies to the user making the request.
        """
        return self.request.user


class PasswordResetView(generics.CreateAPIView):
    """
    API view for password reset.

    This view uses the ResetPasswordSerializer to handle the process
    of password reset requests. It allows any user (including
    unauthenticated ones) to initiate a password reset.
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)


class PasswordResetConfirmView(generics.CreateAPIView):
    """
    API view for confirming a password reset.

    This view uses the ResetPasswordConfirmSerializer to handle the
    process of confirming a password reset request. It allows any user
    (including unauthenticated ones) to confirm their password reset
    using a uid and token.
    """
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        """
        Provide additional context to the serializer.

        This method updates the serializer context with the uid and token
        from the URL kwargs, which are necessary for the password reset
        confirmation process.
        """
        context = super().get_serializer_context()
        token = self.request.query_params.get("token")
        context.update({"token": token})

        return context


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the user's profile.

    This view uses the UserProfileSerializer to handle the retrieval
    and update of the authenticated user's profile information.
    """
    serializer_class = UserProfileSerializer

    def get_object(self):
        """
        Retrieve and return the authenticated user.

        This method ensures that the profile retrieval and update
        operations apply to the user making the request.
        """
        return self.request.user
