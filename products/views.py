from django.contrib.auth import get_user_model
from django.http import request
from rest_framework import generics
from rest_framework.fields import CurrentUserDefault
from .models import Product , CartItem
from .serializers import ProductSerializer , CartitemSerializer 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.models import User
from messenger.models import Message
from django.db.models import Q


class ProductList(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]


    def perform_destroy(self, instance):
        if self.request.user == instance.added_by:
            return super().perform_destroy(instance)
        raise PermissionDenied()

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.added_by:
            return super().perform_update(serializer)
        raise PermissionDenied()
        

class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CartitemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user_id=self.request.user)
class MyProductCartItemsSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CartitemSerializer
    def get_queryset(self):
        queryset = CartItem.objects.filter(product__added_by=self.request.user)
        return queryset
    