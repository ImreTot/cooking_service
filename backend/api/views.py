from djoser.views import UserViewSet

from .serializers import CustomUserSerializer


class CustomUserCreateView(UserViewSet):
    serializer_class = CustomUserSerializer

