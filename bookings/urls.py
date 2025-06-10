from django.urls import path
from . import views

urlpatterns = [
    path('api/bookings/admin/all/', views.BookingAdminListView.as_view(), name='booking-admin-list'),
    path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('api/bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
]