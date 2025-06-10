# impact/serializers.py
from rest_framework import serializers
from .models import ImpactStats

class ImpactStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStats
        fields = ['carbon_saved_kg', 'trees_planted','communities_supported', 'distance_covered_km']
