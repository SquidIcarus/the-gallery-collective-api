from django.urls import path
from .views import ArtworkListView, ArtworkDetailView

urlpatterns = [
    path('', ArtworkListView.as_view()),
    path('<int:pk>/', ArtworkDetailView.as_view()),
]