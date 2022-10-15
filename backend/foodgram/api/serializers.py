from rest_framework import serializers

from recipes.models import (Recipe, Tag, Ingredient, ShopingCart, Favorites,
                            Follow, IngredientQuantity)
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        model = User


class RecipesIngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = Ingredient

    def get_amount(self, obj):
        value = IngredientQuantity.objects.get(ingredient=obj.id)
        return value.amount


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    ingredients = RecipesIngredientSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
        model = Recipe
