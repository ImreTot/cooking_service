from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
