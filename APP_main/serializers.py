from rest_framework import serializers
from .models import CheckupModel


class CheckupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckupModel
        fields = '__all__'
