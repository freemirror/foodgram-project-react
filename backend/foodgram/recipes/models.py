from django.db import models
from colorfield.fields import ColorField

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            null=False)
    color = ColorField(unique=True, blank=False)
    slug = models.SlugField(max_length=200, unique=True,
                            blank=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        null=False
    )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='recipes')
    name = models.CharField(max_length=200, null=False)
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientQuantity'
    )
    text = models.TextField(null=False)
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        default=None
    )
    cooking_time = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        blank=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False
    )
    amount = models.PositiveSmallIntegerField()


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=False
    )


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='basket',
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )


class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
