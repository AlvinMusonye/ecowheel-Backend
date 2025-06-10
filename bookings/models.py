from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    date_booked = models.DateTimeField(auto_now_add=True)
    tour_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    num_guests = models.PositiveIntegerField(default=1)
    tour_name = models.ForeignKey('tours.Tour', on_delete=models.CASCADE, related_name='bookings')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def _str_(self):
        return f"{self.user.username} - {self.tour.title} on {self.tour_date}"



  