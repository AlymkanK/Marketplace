from http.client import responses

from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
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




class ProductListCreateView(APIView):
    serializer_class = ProductsSerializer

    def get(self,  request:Request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductsSerializer(instance=products, manyy=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request:Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                'message': "Product created",
                'data':   serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)