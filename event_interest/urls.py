from django.urls import path
from .views import EventInterestView, EventInterestDetailView

urlpatterns = [
    path('', EventInterestView.as_view()),
    path('<int:pk>/', EventInterestDetailView.as_view()),
]

