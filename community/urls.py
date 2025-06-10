# stories/urls.py

from django.urls import path
from .views import create_story, list_stories

urlpatterns = [
     path('api/stories/create/', create_story, name='create-story'),
    path('api/stories/', list_stories, name='list-stories'),
]
