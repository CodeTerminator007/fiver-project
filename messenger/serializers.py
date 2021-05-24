from rest_framework import serializers
from .models import Message
from products.models import Product
from users.models import User
from djoser.utils import settings
from rest_framework import serializers
from datetime import datetime
import json
from rest_framework.exceptions import NotAcceptable


class MessageSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all(),default=serializers.CurrentUserDefault())
    buyer = serializers.SlugRelatedField(many=False, slug_field='id', queryset=User.objects.all(),)

    product = serializers.SlugRelatedField(
        read_only=False, queryset=Product.objects.all(), slug_field="id")
    seller_name = serializers.SerializerMethodField('get_seller_name') 
    buyer_name = serializers.SerializerMethodField('get_buyer_name')
    class Meta:
        model = Message
        exclude = ('id',)
    
    def get_seller_name(self,Message):
        first_name = Message.seller.first_name
        last_name = Message.seller.last_name
        seller_name = f'{first_name} {last_name}'
        return seller_name

    def get_buyer_name(self,Message):
        first_name = Message.buyer.first_name
        last_name = Message.buyer.last_name
        buyer_name = f'{first_name} {last_name}'
        return buyer_name