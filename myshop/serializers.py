from rest_framework import serializers
from .models import Product, Category, CartItem, Comment, ProductPicture, OrderItem, Order
from django.contrib.auth.models import User
from decouple import config



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['comment_of_reply']

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields['replies'] = CommentSerializer(many=True)
        return fields

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class PictureSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    
    def get_picture(self, obj):
        return config('DOMEN') + obj.picture.url

    class Meta:
        model = ProductPicture
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Product
        exclude = ['quantity_rates',]

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description','price','discount','category', 'supplier']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.Serializer):
    products = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        total_price = 0
        for product in obj['products']:
            total_price += product.price * product.quantity

        return total_price



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"