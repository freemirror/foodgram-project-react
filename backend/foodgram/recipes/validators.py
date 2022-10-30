from rest_framework import serializers


def validate_ingredients(value):
    if len(value) != len(set(list(map(lambda x: x['id'], value)))):
        raise serializers.ValidationError(
            'Нельзя добавлять 2 одинаковых ингредиента'
        )
    return value


def validate_tags(value):
    if len(value) != len(set(value)):
        raise serializers.ValidationError('Нельзя добавлять одинаковые теги')
    return value
