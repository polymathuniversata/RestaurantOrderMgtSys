from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Restaurant, Customer

User = get_user_model()

class UserAdminConfig(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__email', 'phone_number')
    list_filter = ('created_at',)

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register your custom UserAdmin
admin.site.register(User, UserAdminConfig)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Customer, CustomerAdmin)
