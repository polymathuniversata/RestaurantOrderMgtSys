from rest_framework import permissions

class IsCustomerOrRestaurantOwner(permissions.BasePermission):
    """
    Permission to allow only:
    1. The customer who placed the order
    2. The restaurant owner who received the order
    3. Admin users
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have all permissions
        if request.user.is_staff:
            return True
        
        # Check if user is the customer who placed the order
        if hasattr(request.user, 'customer_profile') and obj.customer == request.user.customer_profile:
            return True
        
        # Check if user is the restaurant owner who received the order
        if hasattr(request.user, 'restaurant_profile') and obj.restaurant == request.user.restaurant_profile:
            return True
        
        return False

class IsRestaurantOwner(permissions.BasePermission):
    """
    Permission to allow only the restaurant owner who received the order or admin users.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have all permissions
        if request.user.is_staff:
            return True
        
        # Check if user is the restaurant owner who received the order
        if hasattr(request.user, 'restaurant_profile') and obj.restaurant == request.user.restaurant_profile:
            return True
        
        return False
