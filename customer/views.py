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
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import re
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from labour.models import Labour


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

@api_view(["POST"])
def register_custoumer(request):
    datas = JSONParser().parse(request)
    first = datas["first"]
    last = datas["last"]
    email = datas["email"]
    username = email.split('@')[0]
    password = datas["password"]
    password2 = datas["password2"]

    if not all([first, last, email, password, password2]):
        return Response({"status": "Empty fields"}, status=status.HTTP_400_BAD_REQUEST)

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response({"status": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({"status": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"status": "Email already exists"}, status=status.HTTP_409_CONFLICT)

    if User.objects.filter(username=username).exists():
        return Response({"status": "Username already exists"}, status=status.HTTP_409_CONFLICT)

    user = User.objects.create_user(
        username=username, password=password, email=email, first_name=first, last_name=last)
    cust_profile = Customer.objects.create(user=user)
    cust_profile.save()
    return Response({"status": "Profile created successfully"}, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
            }
        )


#token authentication and get user accordingly to submit review
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def create_review (request):
    datas = JSONParser().parse(request)
    text = datas["text"]
    laborer_id = datas["laborer_id"]
    user = request
    user = user.user
    customer = Customer.objects.get(user=user)
    laborer = Labour.objects.get(id=laborer_id)
    review = Review.objects.create(text=text, laborer=laborer, customer=customer)
    review.save()
    return Response({"status": "Review created successfully"}, status=status.HTTP_201_CREATED)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):  
      queryset = Review.objects.all()
      serializer_class = ReviewSerializer
      permission_classes = [permissions.IsAuthenticated]
