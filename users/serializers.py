from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.StringRelatedField(source='restaurant.title', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'restaurant',
            'restaurant_name',
            'role',
            'is_staff',
            'date_joined',
        )
        read_only_fields = ('date_joined', 'is_staff')
