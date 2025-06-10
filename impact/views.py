from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ImpactStats
from .serializers import ImpactStatsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

def is_admin_or_operator(user):
    return user.is_staff or hasattr(user, 'operatorprofile')

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_impact_stats(request):
    if request.method == 'GET':
        try:
            impact = ImpactStats.objects.get(user=request.user)
            serializer = ImpactStatsSerializer(impact)
            return Response(serializer.data)
        except ImpactStats.DoesNotExist:
            return Response({"detail": "Impact stats not found."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        if not is_admin_or_operator(request.user):
            return Response({'detail': 'Only admins or operators can create impact stats.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("user")
        if not user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImpactStatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        if not is_admin_or_operator(request.user):
            return Response({'detail': 'Only admins or operators can update impact stats.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get("user")
        if not user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            impact = ImpactStats.objects.get(user__id=user_id)
        except ImpactStats.DoesNotExist:
            return Response({"detail": "Impact stats not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImpactStatsSerializer(impact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
