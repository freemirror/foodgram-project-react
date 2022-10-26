from rest_framework import viewsets

from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer)
from recipes.models import Tag, Ingredient, Recipe
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        elif self.action in ('destroy', 'update', 'create'):
            return RecipeWriteSerializer

    # def perform_create(self, serializer):
        # serializer.save(author=self.request.user)

