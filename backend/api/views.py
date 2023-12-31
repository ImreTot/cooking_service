from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.tools import (form_ingredients_list,
                        generate_ingredients_list_via_pdf,
                        get_user_and_recipe_or_404)
from recipes.models import (Ingredient, Recipe, RecipeIngredient, ShoppingCart,
                            Subscription, Tag)
from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import PageLimitPagination
from .serializers import (IngredientSerializer, RecipeInFavoriteSerializer,
                          RecipeSerializer, ShortRecipeInFavoriteSerializer,
                          ShortSubscriptionSerializer, SubscriptionSerializer,
                          TagSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageLimitPagination

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        paginator = self.paginate_queryset(
            User.objects.filter(subscribers__follower=self.request.user)
        )
        serializer = SubscriptionSerializer(paginator,
                                            many=True,
                                            context={'request': self.request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        data = {'follower': request.user.id,
                'following': self.get_object().id}
        serializer = ShortSubscriptionSerializer(
            data=data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        user = request.user
        subscription = get_object_or_404(Subscription,
                                         following=id,
                                         follower=user)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        user = request.user
        recipe = self.get_object()
        data = {'user': user.id,
                'recipe': recipe.id}
        serializer = ShortRecipeInFavoriteSerializer(
            data=data,
            context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        user, recipe = get_user_and_recipe_or_404(request, pk)
        favorite_recipe = user.favorite_recipes.filter(recipe=recipe)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'This recipe is not in the favorites list'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user, recipe = get_user_and_recipe_or_404(request, pk)
        recipe_in_shopping_cart = user.recipes_in_shopping_cart.filter(
            recipe=recipe
        )
        if recipe_in_shopping_cart.exists():
            return Response(
                {'This recipe is already in shopping cart.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = RecipeInFavoriteSerializer(
            recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        user, recipe = get_user_and_recipe_or_404(request, pk)
        recipe_in_shopping_cart = user.recipes_in_shopping_cart.filter(
            recipe=recipe
        )
        if not recipe_in_shopping_cart.exists():
            return Response({
                'error': 'This recipe is not in the shopping_cart'
            },
                status=status.HTTP_400_BAD_REQUEST)
        recipe_in_shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_by__user=user).values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        ingredients_list = form_ingredients_list(ingredients)
        return generate_ingredients_list_via_pdf(ingredients_list)
