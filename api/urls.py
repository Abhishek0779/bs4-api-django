from django.urls import path
from .views import *

urlpatterns = [
   path('getmovies/',get_movies_from_imdb),
   path('get/',get_details),
   path('',movie_detailsListCreateAPIView.as_view(),name="movies_list_create_view"),
   path('<int:id>/edit/',movie_detailsRetrieveUpdateDestroyAPIView.as_view(),name="movies_detail"),
]