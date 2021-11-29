"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Serializer to convert model objects to JSON data
"""

from rest_framework import serializers
from .models import Event, Clock


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'workStatus', 'duration']


class ClockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['type', 'timeValue', 'violationStatus']
