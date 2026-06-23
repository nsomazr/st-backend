from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'description', 'icon', 'image',
            'price_from', 'is_active',
        )
