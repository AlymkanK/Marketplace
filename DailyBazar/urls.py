

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from users_app.urls import router as users_router
from cart_app.urls import router as cart_router
from orders_app.urls import router as orders_router
#from payments_app.urls import router as payments_router
from products_app.urls import router as products_router

router = DefaultRouter()

router.registry.extend(users_router.registry)
router.registry.extend(cart_router.registry)
router.registry.extend(orders_router.registry)
#router.registry.extend(payments_router.registry)
router.registry.extend(products_router.registry)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),

    # main routes
    path('api/', include(router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/drf-auth/', include('rest_framework.urls'))

]

