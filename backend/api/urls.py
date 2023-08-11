from djoser.views import UserViewSet
from django.urls import path, include
from rest_framework import routers

from .views import CustomUserCreateView, TagViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('users/', CustomUserCreateView.as_view({'post': 'create', 'get': 'list'})),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]