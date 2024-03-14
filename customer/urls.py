#urls.py for corresponding views

from django.urls import path
from customer import views

urlpatterns = [
   path('customers/', views.CustomerList.as_view(), name='customer_list'),
   path('customers/<int:pk>/', views.CustomerDetail.as_view(), name='customer_detail'),
   path('laborbookings/', views.LaborBookingList.as_view(), name='laborbooking_list'),
   path('laborbookings/<int:pk>/', views.LaborBookingDetail.as_view(), name='laborbooking_detail'),
   path('users/', views.register_custoumer, name='user_create'),
   path("api-token-auth/", views.CustomAuthToken.as_view(), name="api_token_auth"),
   path('reviews/', views.create_review, name='review_list'),
   path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review_detail'),
]