from .models import Cart, Favourites, CartItem
from rest_framework import serializers
from products_app.serializers import ProductsSerializer


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = ProductsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, cart):
        return cart.get_total_price

class  CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        attribute_value = self.validated_data['attribute_value']

        try:
            cart_item = CartItem.objects.get(
                product =  product,
                cart_id = cart_id,
                attribute_value = attribute_value)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance  = cart_item
        except CartItem.DoesNotExist:
            self.instance  = CartItem.objects.create(cart_id=cart_id,**kwargs)
        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'quantity']

class FavouritesSerializer(serializers.Serializer):
    class Meta:
        model = Favourites
        fields = '__all__'

