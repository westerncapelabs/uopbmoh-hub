from django.contrib.auth.models import User, Group
from .models import Clinician
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ClinicianSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Clinician
        read_only_fields = ('created_by', 'updated_by')
        fields = ('url', 'id', 'msisdn', 'source', 'site', 'extra',
                  'created_at', 'created_by', 'updated_at', 'updated_by')
