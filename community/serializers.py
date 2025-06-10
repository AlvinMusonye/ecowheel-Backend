
from rest_framework import serializers
from .models import Story


class StorySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True) # Assuming your User model has a 'username' field

    class Meta:
        model = Story
        fields = ['id', 'author', 'author_name', 'title', 'content', 'image', 'created_at']
        read_only_fields = ['created_at'] # 'author' is set by the view on create, 'author_name' is derived
