from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User
from recipes.models import Recipe, Subscribe


class CustomUserSerializer(UserCreateSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribe')

    def get_is_subscribe(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        author = get_object_or_404(User, username=obj.username)
        subscriber = get_object_or_404(User, username=request.user.username)
        return Subscribe.objects.filter(author=author.id,
                                        subscriber=subscriber.id).exists()


class AuthorRecipeSerializator(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Subscribe
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            subscriber=obj.subscriber, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        # request = self.context.get('request')
        queryset = Recipe.objects.filter(author=obj.author)
                                                                        #Добавить ограничение на выдачу
        return AuthorRecipeSerializator(queryset, many=True).data
