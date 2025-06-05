from rest_framework import serializers
from .models import Order, OrderItem
from cart_app.models import Cart
from datetime import datetime


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'created_at', 'updated_at')


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Order
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField()
    class Meta:
        model = Order
        fields = (
            'cart_id', 'payment_method', 'order_note',
            'shipping_price')

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('This cart_id is invalid.')
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Sorry your cart is empty.')

        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            payment_method = self.validated_data['payment_method']
            order_note = self.validated_data['order_note']
            shipping_price = self.validated_data['shipping_price']

            user = self.context['user']

            # (1) Create order
            order = Order.objects.create(
                user=user, payment_method=payment_method,
                order_note=order_note, shipping_price=shipping_price)


            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_items = [
                OrderItem(order=order, product=item.product,
                          quantity=item.quantity) for item in cart_items]
            OrderItem.objects.bulk_create(order_items)

            # (4) Business logic (total, order_number etc.)

            total = 0
            order_number = ''
            for item in order_items:
                total += item.product.price_new * item.quantity
                order_number += f"{item.product.product_name[0]}" \
                                f"{item.product.category.category_name[0]}" \
                                f"{item.product.brand.brand_name[0]}"
                item.product.stock_qty -= item.quantity
                item.product.save()

            order.total_price = (total + order.tax.value_tax +
                                 order.shipping_price)
            now = datetime.now()
            order.order_number = f"{order_number.upper()}" \
                                 f"{now.strftime('%Y%m%H%M%S')}"
            order.save()
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)