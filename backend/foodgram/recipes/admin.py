from django.contrib import admin

from .models import (Recipe, Tag, Ingredient, IngredientQuantity,
                     RecipeTag, ShopingCart, Favorites, Follow)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    extra = 1


class IngredientQuantityInLine(admin.TabularInline):
    model = IngredientQuantity
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeTagInLine, IngredientQuantityInLine)
    fields = ('name', 'author', 'text', 'cooking_time', 'image',
              'favorites_count')
    readonly_fields = ('favorites_count',)

    def favorites_count(self, obj):
        return Favorites.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'tag')


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Follow)
class Follow(admin.ModelAdmin):
    list_display = ('user', 'following')
