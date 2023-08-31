from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from djoser.views import UserViewSet

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, SubscriptionSerializer)
from recipes.models import Tag, Ingredient, Recipe, Subscription

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscriptions__following=user)
        serializer = SubscriptionSerializer(queryset,
                                            many=True,
                                            context={'request':
                                                         request})
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        follower = self.get_object()
        Subscription.objects.create(
            following_id=id,
            follower=user
        )
        serializer = SubscriptionSerializer(
            follower,
            context={'request': request}
        )
        return Response(serializer.data, status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        user = request.user
        Subscription.objects.get(
            following=user,
            follower_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
