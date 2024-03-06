from django.urls import path
from .views import MatchLabourersAPIView

urlpatterns = [
      path('match-laborers/', MatchLabourersAPIView.as_view(), name='match-laborers'),
]
