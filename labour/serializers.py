from .models import WorkCategory, Labour
from rest_framework import serializers

class WorkCategorySerializer(serializers.ModelSerializer):
      class Meta:
         model = WorkCategory
         fields = '__all__'

class LabourSerializer(serializers.ModelSerializer):
      class Meta:
         model = Labour
         fields = '__all__'