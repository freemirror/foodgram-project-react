import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, IngredientQuantity, Recipe,
                            RecipeTag, ShoppingCart, Tag)
from recipes.validators import validate_ingredients, validate_tags
from rest_framework import serializers

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


class IngredientQuantitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientQuantitySerializer(
        read_only=True, many=True, source='ingredientquantity_set'
    )
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe

    def __in_entity(self, obj, model):
        request = self.context.get('request')
        return model.objects.filter(
            user=request.user.id,
            recipe=obj.id
        ).exists() and (request and not request.user.is_anonymous)

    def get_is_favorited(self, obj):
        return self.__in_entity(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.__in_entity(obj, ShoppingCart)

    def create_ingredient_quantity(self, valid_ingredients, recipe):
        for ingredient_with_amount in valid_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=ingredient_with_amount.get('id'))
            IngredientQuantity.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_with_amount.get('amount'))

    def create_tags(self, valid_tags, recipe):
        for tag_data in valid_tags:
            tag = get_object_or_404(
                Tag, id=tag_data)
            RecipeTag.objects.create(
                recipe=recipe,
                tag=tag)

    def create(self, validated_data):
        valid_ingredients = validated_data.pop('ingredients')
        valid_tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_tags(valid_tags, recipe)
        self.create_ingredient_quantity(valid_ingredients, recipe)
        return recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        valid_ingredients = validate_ingredients(ingredients)
        valid_tags = validate_tags(tags)
        data['ingredients'] = valid_ingredients
        data['tags'] = valid_tags
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        valid_ingredients = validated_data.get('ingredients',
                                               instance.ingredients)
        valid_tags = validated_data.get('tags', instance.tags)
        IngredientQuantity.objects.filter(recipe__in=[instance.id]).delete()
        RecipeTag.objects.filter(recipe__in=[instance.id]).delete()
        self.create_tags(valid_tags, instance)
        self.create_ingredient_quantity(valid_ingredients, instance)
        return instance


class RecipeActionSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
