from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from .views import CartViewSet, CartItemVIewSet

app_name = 'cart_app'

router = DefaultRouter()
router.register('carts', CartViewSet, basename='cart')




urlpatterns = [
    path('', include(router.urls), name='cart')
]