from rest_framework import serializers
import base64

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from recipes.models import (Recipe, Tag, Ingredient, ShopingCart, Favorites,
                            Subscribe, IngredientQuantity)
from users.models import User
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
        )

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientAmountSerializer(many=True,
                                             source='ingredientquantity_set')
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = get_object_or_404(User, username=request.user.username)
        recipe = get_object_or_404(Recipe, id=obj.id)

        return Favorites.objects.filter(user=user.id,
                                        recipe=recipe.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = get_object_or_404(User, username=request.user.username)
        recipe = get_object_or_404(Recipe, id=obj.id)

        return ShopingCart.objects.filter(user=user.id,
                                          recipe=recipe.id).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('ingredients', 'tags', 'image', 'name', 'cooking_time', 'author')
        model = Recipe
