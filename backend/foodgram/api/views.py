from rest_framework import viewsets

from .serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# class UserViewSet()