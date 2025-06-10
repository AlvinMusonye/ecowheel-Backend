from rest_framework import serializers
from .models import PhotoPost, Like, Comment

class PhotoPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PhotoPost
        fields = ['id', 'user', 'image', 'image_url', 'caption', 'created_at', 'likes_count', 'comments_count', 'reposted_from']
        read_only_fields = ['user', 'created_at']

    def get_image_url(self, obj):
        # This ensures you return the actual URL string from CloudinaryField
        if obj.image:
            return obj.image.url
        return None
