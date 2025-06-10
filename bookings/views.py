from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    """
    List bookings of the authenticated user and allow creating new bookings.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only bookings of the logged-in user
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the booking with the current user assigned
        serializer.save(user=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a booking owned by the authenticated user.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow actions on bookings owned by the user
        return Booking.objects.filter(user=self.request.user)


class BookingAdminListView(generics.ListAPIView):
    """
    List all bookings, accessible only to admin users.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]
