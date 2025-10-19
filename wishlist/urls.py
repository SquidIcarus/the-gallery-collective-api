from django.urls import path
from .views import WishlistView, WishlistDetailView

urlpatterns = [
    path('', WishlistView.as_view()),
    path('/', WishlistDetailView.as_view()),
]