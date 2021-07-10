from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .models import Product, Comment, CartItem, Category, ProductPicture
from .serializers import ProductSerializer, CommentSerializer, CartItemSerializer, CategorySerializer, CartSerializer, ProductCreateSerializer, PictureSerializer, CommentCreateSerializer
from django.contrib.auth.models import User


def get_object(obj, pk):
    try:
        return obj.objects.get(pk=pk)
    except obj.DoesNotExist:
        raise Http404

class ProductsListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object(Product, pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object(Product, pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        product = get_object(Product, pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductPicturesListView(APIView):

    def get(self, request, pk):
        pictures = ProductPicture.objects.filter(product=pk)
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        picture = request.data['picture']
        ProductPicture.objects.create(product=Product.objects.get(id=pk), picture=picture)
        return Response(status=status.HTTP_201_CREATED)


class ProductPictureDetailView(APIView):
    def get(self, request, pk, alt_pk):
        picture = ProductPicture.objects.get(id=alt_pk)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        picture = ProductPicture.objects.get(id=alt_pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     

class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object(Category, pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def delete(self, request, pk):
        category = get_object(Category, pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        category = get_object(Category, pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentsView(APIView):
    def get(self, request, pk):
        comments = Comment.objects.filter(comment_of_reply=None, product=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        if request.data.get('rate') and request.data.get('comment_of_reply'):
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    def get(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        serializer = CommentCreateSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.filter(status=True)
        serializer = CartSerializer({'products':cart_items})
        return Response(serializer.data)



