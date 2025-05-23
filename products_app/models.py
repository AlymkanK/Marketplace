from django.db import models

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Url-имя')
    name = models.CharField(max_length=100, verbose_name='название категории')
    image = models.ImageField(upload_to='products/', verbose_name='фото категории')

class Brand(models.Model):
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Url-имя')
    name = models.CharField(max_length=100, verbose_name='название бренда')
    logo = models.ImageField(upload_to='products/', verbose_name='лого бренда')
    description = models.TextField(verbose_name='описание бренда')

class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Url-имя')
    description = models.TextField(max_length=200, verbose_name='Описание')
    is_on_sale = models.BooleanField(default=True, verbose_name='Скидка')
    quantity = models.IntegerField( verbose_name='Количеество')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Скидка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Бренды'
    )
    image = models.ImageField(upload_to='products/', verbose_name='Фото продукта')