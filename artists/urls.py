from django.urls import path
from .views import ArtistListView, ArtistDetailView, ArtistArtworksView, ArtistEventsView

urlpatterns = [
    path('', ArtistListView.as_view()),
    path('<int:pk>/', ArtistDetailView.as_view()),
    path('<int:pk>/artworks/', ArtistArtworksView.as_view()),
    path('<int:pk>/events/', ArtistEventsView.as_view()),
]

