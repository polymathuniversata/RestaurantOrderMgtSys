from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    OrderItemSerializer
)
from .permissions import IsCustomerOrRestaurantOwner, IsRestaurantOwner

class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for orders."""
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]  # Any authenticated user (will filter in serializer)
        else:
            permission_classes = [permissions.IsAuthenticated, IsCustomerOrRestaurantOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        
        # If user is a restaurant, show only their orders
        if hasattr(user, 'restaurant_profile'):
            return Order.objects.filter(restaurant=user.restaurant_profile)
        
        # If user is a customer, show only their orders
        elif hasattr(user, 'customer_profile'):
            return Order.objects.filter(customer=user.customer_profile)
        
        # Otherwise, return empty queryset
        return Order.objects.none()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'create' and 'order' in self.kwargs:
            context['order'] = self.kwargs['order']
        return context
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Endpoint for updating order status."""
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemViewSet(viewsets.ModelViewSet):
    """API endpoint for order items."""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrRestaurantOwner]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_pk')
        if order_id:
            return OrderItem.objects.filter(order_id=order_id)
        return OrderItem.objects.none()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'order_pk' in self.kwargs:
            context['order'] = Order.objects.get(pk=self.kwargs['order_pk'])
        return context
