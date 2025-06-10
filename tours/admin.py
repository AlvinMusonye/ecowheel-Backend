from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'price','description')
    search_fields = ('title', 'location')
    list_filter = ('date', 'location')
