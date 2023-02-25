from rest_framework import serializers
from .models import Card, Product, Order


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

