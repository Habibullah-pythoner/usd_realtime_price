from rest_framework import serializers
from .models import prices  # Import your 'prices' model here

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = prices
        fields = '__all__'  # Include all fields from the model