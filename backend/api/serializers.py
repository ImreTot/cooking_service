from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Ingredient, Recipe,
                            RecipeIngredient, Tag)

MIN_VALUE = 1
MAX_VALUE = 32000

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username',
                  'first_name', 'last_name')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = request.user
        if not user.is_authenticated:
            return False
        return user.subscriptions.filter(following=obj).exists()


class SubscriptionSerializer(CustomUserSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def validate(self, request):
        user = request['request'].user
        following = self.instance
        if user.subscriptions.filter(following=following).exists():
            raise ValidationError({'error': 'Subscription is already exists.'})
        if user == following:
            raise ValidationError(
                {'error': 'You can\'t subscribe to yourself.'}
            )
        return request

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = RecipeInSubscriptionSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        recipes = obj.recipes.all()
        return recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.IntegerField(min_value=MIN_VALUE,
                                      max_value=MAX_VALUE)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_id(self, obj):
        return obj.ingredient.id

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(min_value=MIN_VALUE,
                                            max_value=MAX_VALUE)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_user(self):
        request = self.context.get('request')
        return request.user

    def get_tags(self, recipe):
        if self.context['request'].method in ['POST', 'PATCH']:
            return recipe.tags.values_list('id', flat=True)
        tags = TagSerializer(recipe.tags.all(), many=True)
        return tags.data

    def get_author(self, obj):
        author = obj.author
        author_serializer = CustomUserSerializer(
            author,
            context=self.context
        )
        return author_serializer.data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return user.favorite_recipes.filter(recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        if user.is_authenticated:
            return user.recipes_in_shopping_cart.filter(
                recipe=obj).exists()
        return False

    def update_or_create_ingredient_amount(self, validated_data, recipe):
        if not validated_data:
            raise serializers.ValidationError({
                'ingredients':
                    'Requires at least one ingredient for the recipe.'})
        recipe_ingredients = [
            RecipeIngredient(
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
                recipe=recipe
            )
            for ingredient in validated_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = self.initial_data.pop('ingredients', '')
        validated_data.pop('ingredients', '')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.update_or_create_ingredient_amount(ingredients_data, recipe)
        return recipe

    def update(self, recipe, validated_data):
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )
        recipe.tags.clear()
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        recipe.ingredients.all().delete()
        self.update_or_create_ingredient_amount(
            self.initial_data.get('ingredients'), recipe)
        recipe.save()
        return recipe


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only = '__all__'

    def validate(self, request):
        user = request['request'].user
        recipe = self.instance
        if recipe.favorited_by.filter(user=user).exists():
            raise ValidationError(
                {'error': 'This recipe is already in favorites.'})
        return request
