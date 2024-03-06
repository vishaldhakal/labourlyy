from .models import Customer, LaborBooking, Review
from rest_framework import serializers
from django.contrib.auth.models import User
from labour.serializers import LabourSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):
      user = UserSerializer()
      class Meta:
         model = Customer
         fields = '__all__'

class LaborBookingSerializer(serializers.ModelSerializer):
      customer = CustomerSerializer()
      laborer = LabourSerializer()

      class Meta:
         model = LaborBooking
         fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
      laborer = LabourSerializer()
      customer = CustomerSerializer()
     
      class Meta:
         model = Review
         fields = '__all__'
