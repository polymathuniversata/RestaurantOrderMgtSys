from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Type
    path('user-type/', views.UserTypeView.as_view(), name='user-type'),
    
    # Profiles
    path('restaurant/profile/', views.RestaurantProfileView.as_view(), name='restaurant-profile'),
    path('customer/profile/', views.CustomerProfileView.as_view(), name='customer-profile'),
]
