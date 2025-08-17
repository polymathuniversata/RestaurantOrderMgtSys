from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Restaurant, Customer

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a profile when a new user is created.
    The actual profile (Restaurant or Customer) should be created in the serializer.
    This is a fallback to ensure profiles exist.
    """
    if created:
        # Only create a profile if one doesn't exist
        if not hasattr(instance, 'restaurant_profile') and not hasattr(instance, 'customer_profile'):
            # Default to creating a customer profile if no type is specified
            Customer.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save the profile when the user is saved."""
    if hasattr(instance, 'restaurant_profile'):
        instance.restaurant_profile.save()
    elif hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
