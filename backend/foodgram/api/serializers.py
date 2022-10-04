from rest_framework import serializers

from recipes.models import (Recipe, Tag, Ingredient, ShopingCart, Favorites,
                            Follow)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
