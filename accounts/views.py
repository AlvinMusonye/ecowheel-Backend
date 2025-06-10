from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsAdminOrOperator, IsAdminOnly
from rest_framework.generics import RetrieveUpdateAPIView

User = get_user_model()

# --- Authentication & Registration ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# --- User Profile Management ---


class UserProfileList(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "count": queryset.count(),
            "profiles": serializer.data,
        }, status=status.HTTP_200_OK)


class UserListAdminView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response({
            "status": "success",
            "count": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)        


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "profile": serializer.data,
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        # Optionally customize the response format on successful update
        if response.status_code == status.HTTP_200_OK:
            return Response({"status": "success", "profile": response.data}, status=status.HTTP_200_OK)
        return response


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Check permissions
    if not IsOwnerOrAdmin().has_object_permission(request, None, user):
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    user.delete()
    return Response({
        "status": "success",
        "message": "User and their profile deleted successfully."
    }, status=status.HTTP_204_NO_CONTENT)


# --- Password Reset Flow ---

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://localhost:5174/reset-password/{uid}/{token}/"

        send_mail(
            'Password Reset - EcoWheel Safari Kenya',
            f'Click the link to reset your password: {reset_url}',
            'no-reply@ecowheel.com',
            [email],
        )
        return Response({'detail': 'Password reset email sent.'})

    except User.DoesNotExist:
        return Response({'detail': 'No user with that email'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    password = request.data.get('password')
    if not password:
        return Response({'detail': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({'detail': 'Password reset successful.'})

    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'detail': 'Invalid user ID or token.'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def whoami(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_admin": user.role == "admin",
        "is_operator": user.role == "operator",
    })

@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])  # Only superusers/staff
def change_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_role = request.data.get('role')

    if new_role not in ['admin', 'operator', 'user']:
        return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

    user.role = new_role
    if new_role == 'admin':
        user.is_staff = True
        user.is_superuser = True
    else:
        user.is_staff = False
        user.is_superuser = False

    user.save()
    return Response({
        "status": "success",
        "message": f"{user.username}'s role updated to {new_role}."
    }, status=status.HTTP_200_OK)


class MyUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "profile": serializer.data,
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "profile": serializer.data,
        }, status=status.HTTP_200_OK)
