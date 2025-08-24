"""
URL configuration for restaurant_order_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Import the schema views
from .schema import urlpatterns as schema_urls

# Schema View for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant Order Management System API",
      default_version='v1',
      description="API for managing restaurant orders, menus, and user accounts.",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=getattr(settings, 'SWAGGER_URL', None),
   patterns=[
       path('api/accounts/', include('accounts.urls')),
       path('api/menu/', include('menu.urls')),
       path('api/orders/', include('orders.urls')),
   ],
   validators=['ssv'],
   generator_class=None,  # Use the default generator
)

# Simple homepage view
def homepage(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Restaurant Order Management System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .api-links {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }
            .api-links a {
                display: block;
                margin: 10px 0;
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
            }
            .api-links a:hover {
                text-decoration: underline;
            }
            .description {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Restaurant Order Management System API</h1>
        <div class="description">
            <p>Welcome to the Restaurant Order Management System API.</p>
            <p>This is a RESTful API for managing restaurant orders, built with Django and Django REST Framework.</p>
        </div>
        
        <div class="api-links">
            <h3>API Documentation</h3>
            <a href="/swagger/">Swagger UI Documentation</a>
            <a href="/redoc/">ReDoc Documentation</a>
            <a href="/api-schema/">Alternative API Schema</a>
            <a href="/api-docs/">Alternative Swagger UI</a>
            <a href="/admin/">Admin Interface</a>
        </div>
        
        <div class="description">
            <h3>Main Features:</h3>
            <ul>
                <li>User authentication (JWT)</li>
                <li>Restaurant and customer profiles</li>
                <li>Menu management</li>
                <li>Order processing</li>
                <li>Admin dashboard</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

urlpatterns = [
    # Homepage
    path('', homepage, name='homepage'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), 
            name='schema-json'),
    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
    
    # Alternative API Schema
    *schema_urls,
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
