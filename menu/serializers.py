from rest_framework import serializers
from .models import MenuCategory, MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('id', 'name', 'description', 'restaurant', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('restaurant', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Set the restaurant to the current user's restaurant profile
        user = self.context['request'].user
        validated_data['restaurant'] = user.restaurant_profile
        return super().create(validated_data)

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    image_url = serializers.ReadOnlyField()
    
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price', 'display_price', 'category', 
                  'category_name', 'restaurant', 'image', 'image_url', 'is_vegetarian', 
                  'is_vegan', 'is_gluten_free', 'is_available', 'preparation_time', 
                  'calories', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('restaurant', 'display_price', 'slug', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Set the restaurant to the current user's restaurant profile
        user = self.context['request'].user
        validated_data['restaurant'] = user.restaurant_profile
        return super().create(validated_data)
    
    def validate_category(self, value):
        # Ensure the category belongs to the restaurant
        user = self.context['request'].user
        if hasattr(user, 'restaurant_profile') and value.restaurant != user.restaurant_profile:
            raise serializers.ValidationError("This category does not belong to your restaurant.")
        return value
