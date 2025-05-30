from django.urls import  path
from .views import SignUpView


app_name = 'users_app'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup')

]