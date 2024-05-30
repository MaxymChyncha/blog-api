from django.urls import path

from user.views import (
    UserRegisterView,
    LoginView,
    LogoutView,
    UserChangePasswordView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
]

app_name = "user"
