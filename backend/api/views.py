from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, CustomUserSerializer)
from recipes.models import Tag, Ingredient, Recipe

User = get_user_model()


class SubscriptionViewSet(ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        subscribed_users = User.objects.filter(subscriptions__following=user)
        return subscribed_users



class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
