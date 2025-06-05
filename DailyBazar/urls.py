"""
URL configuration for DailyBazar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users_app.urls import router as users_router
from cart_app.urls import router as cart_router
from orders_app.urls import router as orders_router
#from payments_app.urls import router as payments_router
from products_app.urls import router as products_router



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/', include(products_router.urls)),
    path('api/auth/', include(users_router.urls)),
    path('api/cart/', include(cart_router.urls)),
    path('api/orders/', include(orders_router.urls)),
    #path('api/payment/', include(payments_router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/drf-auth/', include('rest_framework.urls'))

]

