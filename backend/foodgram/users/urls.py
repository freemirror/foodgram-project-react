from django.urls import path, include
from .views import UserSubscribeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter()

router.register('', UserSubscribeViewSet)
router.register(r'(?P<user_id>\d+)/subscribe',
                UserSubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('users/', include(router.urls)),
]
