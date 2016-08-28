# serializers go here

from .models import FacilityCode
from rest_framework import serializers


class FacilityCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilityCode()
        read_only_fields = ('created_at')
        fields = ('code',)
