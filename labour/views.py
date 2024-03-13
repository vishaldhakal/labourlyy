from rest_framework import generics
from rest_framework import permissions
from .models import WorkCategory, Labour
from .serializers import WorkCategorySerializer, LabourSerializer
import joblib

class WorkCategoryList(generics.ListCreateAPIView):

      queryset = WorkCategory.objects.all()
      serializer_class = WorkCategorySerializer
      

class WorkCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
      
      queryset = WorkCategory.objects.all()
      serializer_class = WorkCategorySerializer
      

class LabourList(generics.ListCreateAPIView): 
      queryset = Labour.objects.all()
      serializer_class = LabourSerializer

class LabourDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = Labour.objects.all()
      serializer_class = LabourSerializer
      