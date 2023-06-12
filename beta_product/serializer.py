from rest_framework import serializers
from .models import UserInterest

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ['id', 'user', 'field']