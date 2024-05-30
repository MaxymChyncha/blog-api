from rest_framework import generics
from rest_framework.permissions import AllowAny

from user.serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
