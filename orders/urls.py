from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:order_pk>/items/', views.OrderItemViewSet.as_view({'get': 'list'}), name='order-items-list'),
    path('<int:order_pk>/items/<int:pk>/', views.OrderItemViewSet.as_view({'get': 'retrieve'}), name='order-item-detail'),
]
