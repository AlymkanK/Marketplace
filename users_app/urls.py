from django.urls import  path
from rest_framework.routers import DefaultRouter
from .views import UserApiView, SMSVerificationApiView

router = DefaultRouter()

router.register(r'user-sign', UserApiView, basename='user-sign')
router.register(r'user-verify', SMSVerificationApiView, basename='user-verify')

urlpatterns = router.urls


