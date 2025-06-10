from rest_framework import serializers
from .models import Booking
from tours.models import Tour

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # Accept tour ID on create/update, not read-only
    tour_name = serializers.SlugRelatedField(
        queryset=Tour.objects.all(),
        slug_field='title'
)

    # Optionally, add this if you want the tour title in response:
    tour_title = serializers.StringRelatedField(source='tour_name', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'date_booked', 'tour_date', 'status', 'num_guests', 'tour_name', 'tour_title', 'amount']
        read_only_fields = ['id', 'date_booked', 'status', 'amount', 'tour_title'] # 'user' is already read-only via its explicit field definition.
