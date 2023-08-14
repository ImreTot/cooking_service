from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'password', 'username',
                  'first_name', 'last_name')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')


class RecipeSerializer(ModelSerializer):
    pass
