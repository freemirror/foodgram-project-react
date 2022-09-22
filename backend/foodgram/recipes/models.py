from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес страницы тэга',
        max_length=200
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField()
    measurement_unit = models.CharField()

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        null=False
    )


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User
    )
    recipes = models.


class


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        null=False
    )
    name = models.CharField(
        max_length=200,
        null=False
    )
    tags = models.models.ManyToManyField(
        Tag,

    )
    ingredients = models.ForeignKey(
        Ingredient
    )
    text = models.TextField(

    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name



