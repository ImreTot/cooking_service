from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from recipes.models import Tag


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')