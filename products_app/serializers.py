from rest_framework import serializers
from .models import Product,Category, Brand, Attribute

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = Attribute
        fields = '__all__'