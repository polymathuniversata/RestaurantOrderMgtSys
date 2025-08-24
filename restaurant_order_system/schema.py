from django.urls import path
from rest_framework.schemas import get_schema_view as rest_schema_view
from rest_framework import permissions
from django.views.generic import TemplateView

schema_view = rest_schema_view(
    title="Restaurant Order Management System API",
    description="API for managing restaurant orders, menus, and user accounts.",
    version="1.0.0",
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Add a view that renders the OpenAPI schema using Swagger UI
swagger_ui_view = TemplateView.as_view(
    template_name='swagger-ui.html',
    extra_context={'schema_url': 'api-schema'}
)

urlpatterns = [
    path('api-schema/', schema_view, name='api-schema'),
    path('api-docs/', swagger_ui_view, name='api-docs'),
]
