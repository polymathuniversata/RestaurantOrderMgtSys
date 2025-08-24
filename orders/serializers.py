from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import MenuItem
from accounts.serializers import CustomerProfileSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.ReadOnlyField(source='menu_item.name')
    
    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_name', 'quantity', 'price', 'special_instructions', 'subtotal')
        read_only_fields = ('price', 'subtotal')
    
    def validate_menu_item(self, value):
        # Check if the menu item belongs to the restaurant associated with the order
        order = self.context['order']
        if value.restaurant != order.restaurant:
            raise serializers.ValidationError("This menu item does not belong to the restaurant.")
        
        # Check if the menu item is available
        if not value.is_available:
            raise serializers.ValidationError("This menu item is currently unavailable.")
        
        return value

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu_item', 'quantity', 'special_instructions')

    def validate_menu_item(self, value):
        # Check if the menu item is available
        if not value.is_available:
            raise serializers.ValidationError("This menu item is currently unavailable.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_details = CustomerProfileSerializer(source='customer', read_only=True)
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'customer', 'customer_details', 'restaurant', 'restaurant_name', 
                  'status', 'status_display', 'delivery_address', 'special_instructions',
                  'total_amount', 'items', 'created_at', 'updated_at')
        read_only_fields = ('customer', 'total_amount', 'created_at', 'updated_at')

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('restaurant', 'delivery_address', 'special_instructions', 'items')
    
    def validate_restaurant(self, value):
        # Check if the restaurant exists and is active
        if not hasattr(value.user, 'restaurant_profile'):
            raise serializers.ValidationError("Invalid restaurant.")
        return value
    
    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items')
        
        # Set the customer to the current user's customer profile
        user = self.context['request'].user
        validated_data['customer'] = user.customer_profile
        
        # Create the order
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in items_data:
            menu_item = item_data['menu_item']
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data['quantity'],
                price=menu_item.price,
                special_instructions=item_data.get('special_instructions', '')
            )
        
        # Calculate the total (will be done in the OrderItem's save method)
        order.save()
        
        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)
    
    def validate_status(self, value):
        # Get the current status
        current_status = self.instance.status
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['accepted', 'cancelled'],
            'accepted': ['preparing', 'cancelled'],
            'preparing': ['ready', 'cancelled'],
            'ready': ['out_for_delivery', 'delivered', 'cancelled'],
            'out_for_delivery': ['delivered', 'cancelled'],
            'delivered': [],  # Terminal state
            'cancelled': [],  # Terminal state
        }
        
        if value not in valid_transitions.get(current_status, []):
            valid_options = ', '.join(valid_transitions.get(current_status, []))
            raise serializers.ValidationError(
                f"Invalid status transition. From '{current_status}', valid options are: {valid_options}"
            )
        
        return value
