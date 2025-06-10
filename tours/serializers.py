from rest_framework import serializers
from .models import Tour
from cloudinary.models import CloudinaryField

class TourSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Tour
        fields = "__all__"
