from rest_framework import serializers
from .models import VDbApi


class VBADataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = VDbApi
        fields = "__all__"