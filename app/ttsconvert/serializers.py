from rest_framework import serializers
from ttsconvert.models import ConversionRequest

class ConversionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequest
        fields = ['id', 'created_at', 'created_by', 'status', 'text_to_convert', 'results']


    def create(self, validated_data):
        return ConversionRequest.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text_to_convert = validated_data.get('text_to_convert', instance.text_to_convert)
        instance.save()
        return instance