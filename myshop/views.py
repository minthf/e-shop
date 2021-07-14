from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from .models import Product, Comment, CartItem, Category, ProductPicture, OrderItem, Order
from .serializers import ProductSerializer, CommentSerializer, CartItemSerializer, CategorySerializer, CartSerializer, ProductCreateSerializer, PictureSerializer, CommentDetailSerializer, OrderItemSerializer, OrderSerializer, CommentPatchSerializer, CartPatchSerializer
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
            serializer.save(supplier=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object(Product, pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object(Product, pk)
        if product.supplier != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        product = get_object(Product, pk)
        if product.supplier != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
        if Product.objects.get(id=pk).supplier != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        picture = request.data['picture']
        ProductPicture.objects.create(product=Product.objects.get(id=pk), picture=picture)
        return Response(status=status.HTTP_201_CREATED)


class ProductPictureDetailView(APIView):
    def get(self, request, pk, alt_pk):
        picture = get_object(ProductPicture, alt_pk)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        if Product.objects.get(id=pk).supplier != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user, product=Product.objects.get(id=pk))
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    def get(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        if Comment.objects.get(id=alt_pk).client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment = get_object(Comment, alt_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, alt_pk):
        if Comment.objects.get(id=alt_pk).client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment = get_object(Comment, alt_pk)
        if comment.comment_of_reply and request.data.get('rate'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentPatchSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.filter(client=request.user)
        serializer = CartSerializer({'products':cart_items})
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          


class CartDetailView(APIView):
    def get(self, request, pk):
        cart_item = get_object(CartItem, pk)

        if CartItem.objects.get(id=pk).client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart_item = get_object(CartItem, pk)
        if CartItem.objects.get(id=pk).client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):    
        cart_item = get_object(CartItem, pk)
        if CartItem.objects.get(id=pk).client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CartPatchSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):
    def post(self, request):
        if not request.data.get('ids') or type(request.data.get('ids')) != list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(id__in=request.data['ids'])
        if not cart_items:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CartSerializer({'products':cart_items})
        order = Order.objects.create(client=User.objects.get(id=1), total_price=serializer.data['total_price'])
        for cart_item in serializer.data['products']:
            print(Product.objects.get(id=cart_item['product']))
            OrderItem.objects.create(
                product=Product.objects.get(id=cart_item['product']),
                order=order,
                quantity=cart_item['quantity'],
                price=cart_item['price']
                )
        for cart_item in cart_items:
            cart_item.delete()
        sserializer = OrderSerializer(order)
        return Response(sserializer.data)


class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

