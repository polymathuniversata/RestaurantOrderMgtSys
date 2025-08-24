from django.db import models
from accounts.models import Customer, Restaurant
from menu.models import MenuItem

class Order(models.Model):
    """Model representing a customer's order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    delivery_address = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.email}"
    
    def save(self, *args, **kwargs):
        # Calculate total amount from order items
        if not self.id:  # Only for new orders
            super().save(*args, **kwargs)  # Save once to get ID
        else:
            # Calculate total from items
            self.total_amount = sum(item.subtotal for item in self.items.all())
            super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Model representing an individual item in an order."""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    menu_item = models.ForeignKey(
        MenuItem, 
        on_delete=models.CASCADE, 
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
    
    @property
    def subtotal(self):
        """Calculate the subtotal for this item."""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        # Set price from menu item if not explicitly set
        if not self.price:
            self.price = self.menu_item.price
        
        # Save the item
        super().save(*args, **kwargs)
        
        # Update order total
        self.order.save()
