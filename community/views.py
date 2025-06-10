from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Story
from .serializers import StorySerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_story(request):
    serializer = StorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_stories(request):
    stories = Story.objects.all()
    serializer = StorySerializer(stories, many=True)
    return Response(serializer.data)