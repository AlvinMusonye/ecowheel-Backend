from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour_date', 'num_guests', 'status', 'date_booked')
    list_filter = ('status', 'tour_date', 'date_booked')
    search_fields = ('user__username',)
    ordering = ('date_booked',)

admin.site.register(Booking, BookingAdmin)
