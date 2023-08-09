from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
