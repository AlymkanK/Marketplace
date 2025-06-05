from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Cart, Favourites, CartItem
from .serializers import CartSerializer, FavouritesSerializer, CartItemSerializer, UpdateCartItemSerializer, AddCartItemSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def  create_cart(self, serializer):
        serializer.save(user=self.request.user)

class CartItemVIewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return  AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

class FavouritesViewSet(ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]