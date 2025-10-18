from django.urls import path
from .views import ArtistListView

urlpatterns = [
    path('', ArtistListView.as_view()),
]

