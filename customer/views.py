from customer.models import Customer, LaborBooking, Review
from rest_framework import generics
from rest_framework import permissions
from customer.serializers import CustomerSerializer, LaborBookingSerializer, UserSerializer, ReviewSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import joblib


class CustomerList(generics.ListCreateAPIView):
      queryset = Customer.objects.all()
      serializer_class = CustomerSerializer
      permission_classes = [permissions.IsAuthenticated]

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = Customer.objects.all()
      serializer_class = CustomerSerializer
      permission_classes = [permissions.IsAuthenticated]

class LaborBookingList(generics.ListCreateAPIView):
      queryset = LaborBooking.objects.all()
      serializer_class = LaborBookingSerializer
      permission_classes = [permissions.IsAuthenticated]

class LaborBookingDetail(generics.RetrieveUpdateDestroyAPIView):
      queryset = LaborBooking.objects.all()
      serializer_class = LaborBookingSerializer
      permission_classes = [permissions.IsAuthenticated]

class UserCreate(generics.CreateAPIView):
      authentication_classes = ()
      permission_classes = ()
      serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
      def post(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          user = serializer.validated_data['user']
          token, created = Token.objects.get_or_create(user=user)
          return Response(token.key)
      
class Logout(APIView):
      permission_classes = (IsAuthenticated,)
      def post(self, request):
          request.user.auth_token.delete()
          return Response(status=status.HTTP_200_OK)
      

class ReviewList(generics.ListCreateAPIView):
      queryset = Review.objects.all()
      serializer_class = ReviewSerializer
      permission_classes = [permissions.IsAuthenticated]

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  
      queryset = Review.objects.all()
      serializer_class = ReviewSerializer
      permission_classes = [permissions.IsAuthenticated]
