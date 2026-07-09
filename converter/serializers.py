from rest_framework import serializers

class ConversionSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    output_format = serializers.ChoiceField(choices=['webp', 'avif'], required=True)
    quality = serializers.IntegerField(min_value=1, max_value=100, default=85)
    width = serializers.IntegerField(min_value=1, required=False)
    height = serializers.IntegerField(min_value=1, required=False)
