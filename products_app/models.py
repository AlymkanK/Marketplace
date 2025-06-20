from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Категория'))
    slug = models.SlugField(unique=True, verbose_name=_('URL'))
    image = models.ImageField(upload_to='categories/', verbose_name=_('Изображение категория'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('brand'))
    slug = models.SlugField(unique=True, verbose_name=_('URL'))
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='brands_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=180, verbose_name=_('Название товара'))
    slug = models.SlugField(unique=True, verbose_name=_('URL'))
    description = models.TextField(verbose_name=_('Описание товара'))
    is_on_sale = models.BooleanField(default=False, verbose_name=_('Акция товара'))
    quantity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('Количество товара'), blank=True)
    discount_price = models.PositiveIntegerField(default=0, verbose_name=_('Скидка на товар в %'), blank=True, validators=[MinValueValidator(0)])
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name=_('Цена товара'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='product_brand')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория товара'), related_name='product_category')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    @property
    def final_price(self):
        from decimal import Decimal
        cache_key = f'product_{self.id}_final_price'
        price = cache.get(cache_key)
        if price is None:
            # Преобразуем discount_price в Decimal перед делением
            discount = Decimal(self.discount_price) / Decimal(100)
            price = round(self.price * (1 - discount), 2) if self.is_on_sale else self.price
            cache.set(cache_key, price, 60 * 60)  # Кэшировать на час
        return price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


@receiver([post_save, post_delete], sender=Product)
def clear_cache_final_price(sender, instance, **kwargs):
    cache_key = f'product_{instance.id}_final_price'
    cache.delete(cache_key)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f'Изображение {self.product.name}'


class Attribute(models.Model):
    TEXT = 'text'
    NUMBER = 'number'
    CHOICE = 'choice'

    TYPE_CHOICES = [
        (TEXT, _('Текст')),
        (NUMBER, _('Число')),
        (CHOICE, _('Выбор')),
    ]

    name = models.CharField(max_length=255, verbose_name=_('Название атрибута'))
    type_attribute = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TEXT, verbose_name=_('Тип аттрибута'))

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='product_attributes')
    value = models.TextField(verbose_name='Значение аттрибута')

    def __str__(self):
        return f'{self.attribute.name}:  {self.value}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_user')
    rating = models.PositiveIntegerField(verbose_name=_('Рейтинг товара'), null=True, blank=True, validators=[MinValueValidator(1)])
    comment = models.TextField(verbose_name=_('Комментарий'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_approved = models.BooleanField(default=False, verbose_name=_('Одобрен'))

    def __str__(self) -> str:
        return f'Отзыв от пользователя: {self.user.username} на продукт: {self.product.name}'

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

'''
review = Review.objects.get(id=1)
review_image = review.images.all()
'''
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='review_images/')

    def __str__(self):
        return f'Изображение к отзыву {self.review.id}'


class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_questions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Вопрос')

    def __str__(self):
        return f'Вопрос от {self.user.username} к {self.product.name}: {self.text[:30]}'

