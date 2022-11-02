from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            ShoppingCart, Tag)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .serializers import (IngredientSerializer, RecipeActionSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def __get_data(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        return relation, recipe

    def add(self, model, user, pk):
        relation, recipe = self.__get_data(model, user, pk)
        if relation.exists():
            return Response(
                {'errors': 'Рецепт уже добавлен!'},
                status=HTTPStatus.BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeActionSerializer(recipe)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def delete_relation(self, model, user, pk):
        relation, recipe = self.__get_data(model, user, pk)
        if not relation.exists():
            return Response(
                {'errors': 'Рецепт уже удалён!'},
                status=HTTPStatus.BAD_REQUEST)
        relation.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    def __change_data(self, model, request, pk):
        user = request.user
        if request.method == 'POST':
            return self.add(model, user, pk)
        if request.method == 'DELETE':
            return self.delete_relation(model, user, pk)
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
        return self.__change_data(Favorite, request, pk)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        return self.__change_data(ShoppingCart, request, pk)

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        queryset = IngredientQuantity.objects.filter(
            recipe__basket__user=user)
        ingredients = queryset.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        shopping_list = ''
        count = 0
        for ingredient in ingredients:
            count += 1
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount__sum']
            shopping_list += (f'{count}. {name} '
                              f'{measurement_unit} - {amount}\n')
        filename = f"{user}_shopping_list.txt"
        content = shopping_list
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response
