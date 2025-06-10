from django.urls import path
from .views import user_impact_stats

urlpatterns = [
    path('api/impact/user/', user_impact_stats, name='user-impact-stats'),
]
