from django.urls import path, include

from .views import CustomUserCreateView

app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls')),
    path('users/', CustomUserCreateView.as_view({'post': 'create'})),
    path('auth/', include('djoser.urls.authtoken')),
]