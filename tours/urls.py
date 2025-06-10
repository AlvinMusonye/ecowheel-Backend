from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('api/tours/', views.tour_list_create, name='tour-list-create'),   # Handles GET (list) and POST (create)
    path('api/tours/<int:pk>/', views.tour_detail, name='tour-detail'),    # Handles GET, PUT, DELETE for individual tours
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
