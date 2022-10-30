from django_filters import AllValuesMultipleFilter, FilterSet
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name="tags__slug")

    class Meta:
        model = Recipe
        fields = ('tags',)
