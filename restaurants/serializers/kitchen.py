from rest_framework import serializers

from restaurants.models import Kitchen


class KitchenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kitchen
        fields = (
            'id',
            'name',
        )
