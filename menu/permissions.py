from rest_framework import permissions

class IsRestaurantOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Restaurant owners to have full control over their own menu items
    - Read-only access for other users
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For POST, PUT, PATCH, DELETE, ensure user has restaurant profile
        return request.user.is_authenticated and hasattr(request.user, 'restaurant_profile')
    
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow restaurant owners to modify their own menu items
        return (request.user.is_authenticated and 
                hasattr(request.user, 'restaurant_profile') and 
                obj.restaurant == request.user.restaurant_profile)
