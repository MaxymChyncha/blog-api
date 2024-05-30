from django.urls import path

from user.views import UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
]

app_name = "user"
