from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register('carts', CartViewSet, basename='cart')

app_name = 'cart_app'

urlpatterns = [
    path('', include(router.urls))
]