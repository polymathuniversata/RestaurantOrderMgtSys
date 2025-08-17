from django.db import models
from django.utils.text import slugify
from accounts.models import Restaurant

class MenuCategory(models.Model):
    """Model representing a category for menu items (e.g., Appetizers, Main Course, Desserts)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='menu_categories'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Menu Categories'
        unique_together = ('name', 'restaurant')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class MenuItem(models.Model):
    """Model representing a single menu item in a restaurant's menu."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        MenuCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='menu_items'
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='menu_items'
    )
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(help_text="Preparation time in minutes", default=15)
    calories = models.PositiveIntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__name', 'name']
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.restaurant.name} {self.name}")
            self.slug = base_slug
            counter = 1
            while MenuItem.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def display_price(self):
        """Return the price formatted with currency."""
        return f"${self.price:.2f}"

    @property
    def image_url(self):
        """Return the URL of the image or a default if none is available."""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/default-food.jpg'  # You'll need to set up this default image
