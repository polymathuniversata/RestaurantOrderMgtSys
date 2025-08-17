from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, 
    CustomTokenObtainPairSerializer,
    RestaurantProfileSerializer,
    CustomerProfileSerializer
)
from .models import Restaurant, Customer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RestaurantProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.restaurant_profile
        except Restaurant.DoesNotExist:
            return Response(
                {"detail": "Restaurant profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.request.user.customer_profile
        except Customer.DoesNotExist:
            return Response(
                {"detail": "Customer profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class UserTypeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        data = {
            'is_restaurant': hasattr(user, 'restaurant_profile'),
            'is_customer': hasattr(user, 'customer_profile')
        }
        return Response(data)
