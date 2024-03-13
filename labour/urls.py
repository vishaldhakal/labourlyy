from django.urls import path
from labour import views

urlpatterns = [
   path('labours/', views.LabourList.as_view(), name='labour_list'),
   path('labours/<int:pk>/', views.LabourDetail.as_view(), name='labour_detail'),
   path('work-category/', views.WorkCategoryList.as_view(), name='work_category_list'),
   path('work-category/<int:pk>/', views.WorkCategoryDetail.as_view(), name='work_category_detail'),
]