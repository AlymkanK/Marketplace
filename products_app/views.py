from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductsSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

class  ProductListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

