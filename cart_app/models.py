from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from products_app.models import Product, Attribute



User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Сессионный ключ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Товар'))
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('Количество'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата добавления'))

    class Meta:
        db_table = 'cart'
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')

        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['created_at']),
        ]

    @property
    def get_total_price(self):
        return self.product.final_price * self.quantity

    @classmethod
    def get_cart_count(cls, user, session_key):
        if user and user.is_authenticated:
            return cls.objects.filter(user=user).count()
        elif session_key:
            return cls.objects.filter(session_key=session_key).count()
        return 0

    def __str__(self):
        return f'Корзина пользователя: {self.user.username} | Товар: {self.product.name} | Количество: {self.quantity}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name = 'корзинаэ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)



# Избранные
class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Сессионный ключ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата добавления'))

    class Meta:
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Избранное пользователя: {self.user.username} | Товар: {self.product.name}'


