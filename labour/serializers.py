from .models import WorkCategory, Labour
from rest_framework import serializers

class WorkCategorySerializer(serializers.ModelSerializer):
      class Meta:
         model = WorkCategory
         fields = '__all__'

class WorkCategorySmalllSerializer(serializers.ModelSerializer):
      class Meta:
         model = WorkCategory
         fields = ['name']
class LabourSerializer(serializers.ModelSerializer):
      work_category = WorkCategorySmalllSerializer()
      class Meta:
         model = Labour
         fields = '__all__'

class LabourDetailSerializer(serializers.ModelSerializer):
      work_category = WorkCategorySerializer()
      reviews = serializers.StringRelatedField(many=True)
      class Meta:
         model = Labour
         fields = '__all__'