from djoser.views import UserViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import ListAPIView

from .serializers import CustomUserSerializer, TagSerializer
from recipes.models import Tag


class CustomUserCreateView(UserViewSet):
    serializer_class = CustomUserSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
