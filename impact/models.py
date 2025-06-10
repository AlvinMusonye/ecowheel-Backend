
from django.db import models
from django.conf import settings

class ImpactStats(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='impact_stats'
    )
    carbon_saved_kg = models.FloatField(default=0.0)
    trees_planted = models.IntegerField(default=0)
    distance_covered_km = models.FloatField(default=0.0)
    communities_supported = models.IntegerField(default=0)

    def __str__(self):
        return f"ImpactStats for {self.user}"
