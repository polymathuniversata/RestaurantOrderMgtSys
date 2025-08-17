from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Restaurant, Customer

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    user_type = serializers.ChoiceField(
        choices=[('restaurant', 'Restaurant'), ('customer', 'Customer')],
        write_only=True
    )
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        validated_data.pop('password2', None)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        if user_type == 'restaurant':
            Restaurant.objects.create(user=user)
        else:
            Customer.objects.create(user=user)
            
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['is_restaurant'] = hasattr(user, 'restaurant_profile')
        token['is_customer'] = hasattr(user, 'customer_profile')
        
        return token

class RestaurantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ('id', 'email', 'name', 'location', 'phone_number', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class CustomerProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'address', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
