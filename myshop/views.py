from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .permissions import OwnerPermission, CartOwnerPermission, IsSupplierPermission, IsClientPermission, IsAdminUserOrReadOnly, ClientPermission
from .models import Product, Comment, CartItem, Category, ProductPicture, OrderItem, Order, User
from .serializers import ProductSerializer, CommentSerializer, CartItemSerializer, CategorySerializer, CartSerializer, ProductCreateSerializer, PictureSerializer, CommentDetailSerializer, OrderItemSerializer, OrderSerializer, CommentPatchSerializer, CartPatchSerializer


def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404




class ProductsListView(APIView):
    permission_classes = [IsSupplierPermission]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [OwnerPermission, IsSupplierPermission]

    def get(self, request, pk):
        product = get_object(Product, pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = get_object(Product, pk)
        self.check_object_permissions(request, product)
        if product.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        product = get_object(Product, pk)
        self.check_object_permissions(request, product)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ProductPicturesListView(APIView):
    permission_classes = [OwnerPermission, IsSupplierPermission]

    def get(self, request, pk):
        pictures = ProductPicture.objects.filter(product=pk)
        serializer = PictureSerializer(pictures, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        product = get_object(Product, pk)
        self.check_object_permissions(request, product)
        picture = request.data['picture']
        ProductPicture.objects.create(product=Product.objects.get(id=pk), picture=picture)
        return Response(status=status.HTTP_201_CREATED)


class ProductPictureDetailView(APIView):
    permission_classes = [OwnerPermission, IsSupplierPermission]

    def get(self, request, pk, alt_pk):
        picture = get_object(ProductPicture, alt_pk)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        product = get_object(Product, pk)
        self.check_object_permissions(request, product)
        picture = ProductPicture.objects.get(id=alt_pk)
        picture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

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
    permission_classes = [IsAdminUserOrReadOnly]

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
    permission_classes = [IsClientPermission]
    
    def get(self, request, pk):
        comments = Comment.objects.filter(comment_of_reply=None, product=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        if request.data.get('rate') and request.data.get('comment_of_reply'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=Product.objects.get(id=pk))
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permission_classes = [OwnerPermission, IsClientPermission]

    def get(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, alt_pk):
        comment = get_object(Comment, alt_pk)
        self.check_object_permissions(request, comment)

        if comment.comment_of_reply and request.data.get('rate'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentPatchSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    permission_classes = [OwnerPermission, ClientPermission]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        serializer = CartSerializer({'products':cart_items})
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)          


class CartDetailView(APIView):
    permission_classes = [CartOwnerPermission, ClientPermission]
    def get(self, request, pk):
        cart_item = get_object(CartItem, pk)
        self.check_object_permissions(request, cart_item)
        if CartItem.objects.get(id=pk).user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart_item = get_object(CartItem, pk)
        self.check_object_permissions(request, cart_item)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):    
        cart_item = get_object(CartItem, pk)
        self.check_object_permissions(request, cart_item)
        serializer = CartPatchSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):
    permission_classes = [CartOwnerPermission]
    def post(self, request):
        if not request.data.get('ids') or type(request.data.get('ids')) != list:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(id__in=request.data['ids'])
        if not cart_items:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        for cart_item in cart_items:
            self.check_object_permissions(request, cart_item)

        serializer = CartSerializer({'products':cart_items})
        order = Order.objects.create(user=request.user, total_price=serializer.data['total_price'])
        for cart_item in serializer.data['products']:
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
    permission_classes = [ClientPermission]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

