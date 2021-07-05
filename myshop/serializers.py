from rest_framework import serializers
from .models import Product, Category, CartItem, Comment, ProductPicture
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

class PictureSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    
    def get_picture(self, obj):
        return config('DOMEN') + obj.picture.url

    class Meta:
        model = ProductPicture
        fields = ['picture']



class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
