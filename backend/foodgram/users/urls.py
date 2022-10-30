from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserSubscribeViewSet

app_name = 'users'

router = DefaultRouter()

router.register('', UserSubscribeViewSet)
router.register(r'(?P<user_id>\d+)/subscribe',
                UserSubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('users/', include(router.urls)),
]
