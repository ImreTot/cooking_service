from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient


class CustomUserSerializer(UserCreateSerializer):
    """
    Custom user serializer replaces standard djoser serializer
    with additional fields 'first_name', 'last_name'.
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'password', 'username',
                  'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        recipe = self.context.get('recipe')
        recipe_ingredient = obj.recipeingredient_set.filter(recipe=recipe)
        if recipe_ingredient:
            return recipe_ingredient.amount
        return None


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False

    def get_ingredients(self, obj):
        ingredients = [rec_ing.ingredient for rec_ing in obj.recipeingredient_set.all()]
        serializer = IngredientInRecipeSerializer(ingredients, many=True, context=self.context)
        print(ingredients)
        return serializer.data
