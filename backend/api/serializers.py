from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient,
                            Favorite, Subscription, ShoppingCart)

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Custom user serializer replaces standard djoser serializer
    with additional fields 'first_name', 'last_name'.
    """
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
        return Subscription.objects.filter(
            follower=user, following=obj).exists()


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

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = RecipeInSubscriptionSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        recipes = obj.recipes.all()
        recipes_numbers = recipes.count()
        return recipes_numbers


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
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_user(self):
        request = self.context.get('request')
        user = request.user
        return user

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

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.all()
        self.context['recipe'] = recipe
        serializer = IngredientInRecipeSerializer(
            ingredients,
            many=True,
            context=self.context
        )
        return serializer.data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.get_user()
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe=obj
            ).exists()
        return False

    def update_or_create_ingredient_amount(self, validated_data, recipe):
        if not validated_data:
            raise serializers.ValidationError({
                'ingredients': 'Requires at least one ingredient for the recipe.'})
        for ingredient in validated_data:
            RecipeIngredient.objects.update_or_create(ingredient_id=ingredient['id'],
                                                      amount=ingredient['amount'],
                                                      recipe=recipe)


    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = self.initial_data.pop('ingredients', '')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.update_or_create_ingredient_amount(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        self.update_or_create_ingredient_amount(self.initial_data.get('ingredients'), instance)
        instance.save()
        return instance


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only = '__all__'
