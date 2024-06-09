from django.urls import path

from user.views import (
    UserRegisterView,
    LoginView,
    LogoutView,
    UserChangePasswordView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserProfileView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]

app_name = "user"
