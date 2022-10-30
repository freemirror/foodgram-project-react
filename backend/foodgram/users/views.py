from http import HTTPStatus

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Subscribe
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import SubscribeReadSerializer


class UserSubscribeViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        subscriber = request.user
        queryset = Subscribe.objects.filter(subscriber=subscriber)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeReadSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        subsciber = request.user
        author = get_object_or_404(User, id=id)
        if author == subsciber:
            return Response({'errors': 'Нельзя подписаться на себя'},
                            status=HTTPStatus.BAD_REQUEST)
        if Subscribe.objects.filter(subscriber=subsciber,
                                    author=author).exists():
            return Response({'errors': 'Подписка уже существует'},
                            status=HTTPStatus.BAD_REQUEST)
        subscribe = Subscribe.objects.create(subscriber=subsciber,
                                             author=author)
        serializer = SubscribeReadSerializer(
            subscribe, context={'request': request}
        )
        return Response(serializer.data, status=HTTPStatus.CREATED)

    @subscribe.mapping.delete
    def delete_issubscribed(self, request, id):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        subscribed = Subscribe.objects.filter(subscriber=subscriber,
                                              author=author)
        if subscribed.exists():
            subscribed.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
