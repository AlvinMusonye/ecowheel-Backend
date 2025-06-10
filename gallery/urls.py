from django.urls import path
from . import views

urlpatterns = [
    path('api/photos/', views.photo_list_create, name='photo-list-create'),
    path('api/photos/<int:pk>/', views.photo_detail, name='photo-detail'),
    path('api/photos/<int:photo_id>/like/', views.like_photo, name='photo-like'),
    path('api/photos/<int:photo_id>/comment/', views.comment, name='photo-comment'),
    path('api/photos/<int:photo_id>/repost/', views.repost_photo, name='photo-repost'),
]
