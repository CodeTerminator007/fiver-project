import re
from messenger.models import Message
from rest_framework import serializers
from .models import Product , CartItem
from categories.models import Category
from users.models import User
from rest_framework import serializers
from drf_base64.fields import Base64ImageField

class ProductSerializer(serializers.ModelSerializer):
    photo1 = Base64ImageField()
    photo2 = Base64ImageField()
    photo3 = Base64ImageField()
    photo4 = Base64ImageField()

    category = serializers.SlugRelatedField(read_only=False, queryset=Category.objects.all(), slug_field="name")
    added_by = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'

class CartitemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField('get_productName')
    product_price = serializers.SerializerMethodField('get_productPrice') 
    product_image = serializers.SerializerMethodField('get_productImage')
    class Meta:
        model = CartItem
        fields = '__all__'

    def get_productName(self,CartItem):
        product_name = CartItem.product.name
        return product_name
    def get_productPrice(self,CartItem):
        product_price = CartItem.product.price
        return product_price 
    def get_productImage(self,CartItem):
        product_image = CartItem.product.photo1.url
        return product_image               

    def validate(self, validated_data):
        product = validated_data.get('product')
        user = validated_data.get('user')
        if CartItem.objects.filter(product=product,user=user).exists() ==True:            
            raise serializers.ValidationError({'Validation Error':'Already added in your Cart'})        
        return validated_data

class CartitemupdateSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField('get_productName')
    product_price = serializers.SerializerMethodField('get_productPrice') 
    product_image = serializers.SerializerMethodField('get_productImage')
    class Meta:
        model = CartItem
        fields = '__all__'

    def get_productName(self,CartItem):
        product_name = CartItem.product.name
        return product_name
    def get_productPrice(self,CartItem):
        product_price = CartItem.product.price
        return product_price 
    def get_productImage(self,CartItem):
        product_image = CartItem.product.photo1.url
        return product_image               
    def validate(self, validated_data):
        if validated_data["seller_confirmation"] == "Sold" and validated_data["buyer_confirmation"] == "Sold":
            validated_data["status"] = "Sold"
            return validated_data
        elif validated_data["seller_confirmation"] == "Sold" and validated_data["buyer_confirmation"] == "Cancelled":
            validated_data["status"] = "Cancelled"            
            return validated_data
        elif validated_data["seller_confirmation"] == "Cancelled" and validated_data["buyer_confirmation"] == "Sold":
            validated_data["status"] = "Cancelled"            
            return validated_data
        elif validated_data["seller_confirmation"] == "Cancelled" and validated_data["buyer_confirmation"] == "Cancelled":
            validated_data["status"] = "Cancelled"            
            return validated_data
        elif validated_data["seller_confirmation"] == "Pending" and validated_data["buyer_confirmation"] == "Cancelled":
            validated_data["status"] = "Cancelled"            
            return validated_data
        elif validated_data["seller_confirmation"] == "Cancelled" and validated_data["buyer_confirmation"] == "Pending":
            validated_data["status"] = "Cancelled"            
            return validated_data
        elif validated_data["seller_confirmation"] == "Pending" and validated_data["buyer_confirmation"] == "Pending":
            validated_data["status"] = "Pending"            
            return validated_data            

        return validated_data        

