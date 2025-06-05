from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Order
from .serializers import *


class OrderViewSet(viewsets.ModelViewSet):
    class Meta:
        model = Order
        fields = '__all__'

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminUser]
        return [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        http_method_names = ['get', 'post', 'patch', 'delete']
        search_fields = ('order_number', 'status')
        ordering_fields = (
            'user', 'shipping_price', 'total_price',
            'tax', 'status', 'created_at')

        def get_permissions(self):
            if self.request.method in ['PATCH']:
                return [IsAdminUser()]
            return [IsAuthenticated()]

        def create(self, request, *args, **kwargs):
            context = {'user': self.request.user}
            serializer = CreateOrderSerializer(
                data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer