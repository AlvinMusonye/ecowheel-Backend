from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Tour
from .serializers import TourSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
@parser_classes([JSONParser, MultiPartParser, FormParser])  # <-- allow JSON and multipart/form-data
def tour_list_create(request):
    if request.method == 'GET':
        tours = Tour.objects.all()
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','PATCH', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
@parser_classes([JSONParser, MultiPartParser, FormParser])  # <-- allow JSON and multipart/form-data
def tour_detail(request, pk):
    try:
        tour = Tour.objects.get(pk=pk)
    except Tour.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TourSerializer(tour)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TourSerializer(tour, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':  # <-- Add this block
        serializer = TourSerializer(tour, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)