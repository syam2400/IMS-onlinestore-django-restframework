from rest_framework import serializers
from stocks.models import *

class Subvariant_serilizers(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['option']


class Variant_serilizers(serializers.ModelSerializer):
    subvariants = Subvariant_serilizers(many=True)

    class Meta:
        model = Variant
        fields = ['variant_name','subvariants']

class Product_Serilizer(serializers.ModelSerializer):
    variants = Variant_serilizers(many=True)

    class Meta:
        model = Products
        fields = ['ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedUser', 'IsFavourite', 'Active', 'HSNCode', 'TotalStock', 'variants']
    
    def create(self,validated_data):
        variant_datas = validated_data.pop("variants",[]) 
        product_obj = Products.objects.create(ProductID=validated_data.get('ProductID'),
                                              ProductCode=validated_data.get('ProductCode'),
                                              ProductName=validated_data.get('ProductName'),
                                              ProductImage=validated_data.get('ProductImage'),
                                              CreatedUser=validated_data.get('CreatedUser'),
                                              IsFavourite=validated_data.get('IsFavourite'),
                                              Active=validated_data.get('Active'),
                                              HSNCode=validated_data.get('HSNCode'),
                                              TotalStock=validated_data.get('TotalStock'))
        # print(product_obj,variant_datas)

        for data in variant_datas:
            subvariant_datas = data.pop("subvariants",[])
            # print(subvariant_datas,data)

            variant_obj = Variant.objects.create(product=product_obj, **data)
            for subvariant in subvariant_datas:
                SubVariant.objects.create(variant=variant_obj, **subvariant)
        return product_obj
        
        
class StockUpdateSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    ProductCode = serializers.CharField(max_length=100)
    variant_typ = serializers.CharField(max_length=100)
    option = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField(required=False, allow_null=True)

    
    def validate_quantity(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        if 'quantity' not in data and self.context['request'].method != 'DELETE':
            raise serializers.ValidationError("Quantity is required for non-delete operations.")
        return data