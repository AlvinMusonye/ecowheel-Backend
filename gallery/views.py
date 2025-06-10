from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import PhotoPost, Like, Comment
from .serializers import PhotoPostSerializer

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def photo_list_create(request):
    if request.method == 'GET':
        photos = PhotoPost.objects.all().order_by('-created_at')
        serializer = PhotoPostSerializer(photos, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PhotoPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def photo_detail(request, pk):
    try:
        photo = PhotoPost.objects.get(pk=pk)
    except PhotoPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PhotoPostSerializer(photo)
        return Response(serializer.data)

    if request.method == 'PUT':
        if photo.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PhotoPostSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if photo.user != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_photo(request, photo_id):
    try:
        photo = PhotoPost.objects.get(id=photo_id)
    except PhotoPost.DoesNotExist:
        return Response({'detail': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(user=request.user, photo=photo)
    if not created:
        return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Liked successfully'})


@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
def comment(self, request, pk=None):
    photo = self.get_object()
    text = request.data.get('text')

    if not text:
        return Response({'error': 'Comment text is required.'}, status=400)

    Comment.objects.create(photo=photo, user=request.user, text=text)
    return Response({'message': 'Comment added successfully.'}, status=201)


   


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def repost_photo(request, photo_id):
    try:
        original = PhotoPost.objects.get(pk=photo_id)
    except PhotoPost.DoesNotExist:
        return Response({'detail': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

    caption = request.data.get('caption', '')
    repost = PhotoPost.objects.create(
        user=request.user,
        image=original.image,
        caption=caption,
        reposted_from=original
    )
    serializer = PhotoPostSerializer(repost)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
