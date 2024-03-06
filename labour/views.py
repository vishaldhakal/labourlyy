from rest_framework import generics
from rest_framework import permissions
from .models import WorkCategory, Labour
from .serializers import WorkCategorySerializer, LabourSerializer
import joblib

class WorkCategoryList(generics.ListCreateAPIView):

      queryset = WorkCategory.objects.all()
      serializer_class = WorkCategorySerializer
      permission_classes = [permissions.IsAuthenticated]

class WorkCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
      
      queryset = WorkCategory.objects.all()
      serializer_class = WorkCategorySerializer
      permission_classes = [permissions.IsAuthenticated]

class LabourList(generics.ListCreateAPIView): 
      queryset = Labour.objects.all()
      serializer_class = LabourSerializer
      permission_classes = [permissions.IsAuthenticated]

class LabourDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = Labour.objects.all()
      serializer_class = LabourSerializer
      permission_classes = [permissions.IsAuthenticated]