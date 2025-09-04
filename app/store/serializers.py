from rest_framework import serializers
from .models import Product,Collection
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    """
    need to redefine id, title, and unit_price 
    inside the serializer when using ModelSerializer — 
    DRF
    """
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    #collection = serializers.StringRelatedField()
    #collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # to use make this appear more like nested json - add serializers to CollectionSerializer
    #collection = CollectionSerializer()
    # to list collection as Hyperlink
    collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),\
                                                     view_name ='collection-detail')

    class Meta:
        model = Product
        fields = ['id', 'title','price','price_with_tax','collection']

    def get_price_with_tax(self, product:Product):
           return product.unit_price * Decimal('1.1')
    
    # def validate(self,data):
    #     if data['password'] != data['confirm password']:
    #          return serializers.ValidationError("Password don't match")
    #     return data
    
    