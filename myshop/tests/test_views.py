from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myshop.models import Product, Category, CartItem, Comment, ProductPicture, OrderItem, Order, User
from rest_framework.test import APIClient


class AccountTests(APITestCase):

    def test_create_client_account(self):
        url = reverse('user-list')
        data = {'username': 'DabApps', 'password': '132132132arstarstra'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'DabApps')
        self.assertEqual(User.objects.get().is_supplier, False)

    def test_create_supplier_account(self):
        url = reverse('user-list')
        data = {'username': 'DabApps', 'password': '132132132arstarstra', 'is_supplier': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'DabApps')
        self.assertEqual(User.objects.get().is_supplier, True)


    def test_get_token_without_email_verification_(self):
        url = reverse('jwt-create')
        User.objects.create(username='mint', password='12345')
        data = {'username': 'mint', 'password': '12345'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'mint')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_token_with_email_verification_(self):
        url = reverse('user-list')
        data = {'username': 'DabApps', 'password': '132132132arstarstra', 'is_supplier': True}
        response = self.client.post(url, data, format='json')
        user = User.objects.get()
        user.is_active = True
        user.save()
        url = reverse('jwt-create')
        data = {'username': 'DabApps', 'password': '132132132arstarstra'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductListViewTest(APITestCase):

    def test_get_product_list_supplier(self):
        url = reverse('products-list')
        user = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_list_supplier(self):
        url = reverse('products-list')
        user = User.objects.create(username='mint', password='12345')
        self.client.force_authenticate(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_product_supplier(self):
        url = reverse('products-list')
        user = User.objects.create(username='mint', password='12345', is_supplier=True)
        category = Category.objects.create(title='123', description='123')
        self.client.force_authenticate(user)
        data = {'title': '123', "description": '123', "price": 123, 'category': category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       

    def test_post_product_client(self):
        url = reverse('products-list')
        user = User.objects.create(username='mint', password='12345')
        category = Category.objects.create(title='123', description='123')
        self.client.force_authenticate(user)
        data = {'title': '123', "description": '123', "price": 123, 'category': category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 


class ProductDetailViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345', is_supplier=True)
        self.product1 = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.product2 = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user3)


    def test_get_product_supplier(self):
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_client(self):
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_own_product(self):
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_authenticate(self.user1)
        data = {'title':'qwf', 'description':'rst'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_not_own_product(self):
        url = reverse('product-detail', args=(self.product2.id,))
        self.client.force_authenticate(self.user1)
        data = {'title':'qwf', 'description':'rst'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_product(self):
        url = reverse('product-detail', args=(self.product1.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_own_product(self):
        url = reverse('product-detail', args=(self.product2.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentsViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.product1 = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)

    def test_get_comments_supplier(self):
        url = reverse('comments-of-product', args=(self.product1.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comments_client(self):
        url = reverse('comments-of-product', args=(self.product1.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comments_supplier(self):
        url = reverse('comments-of-product', args=(self.product1.id,))
        self.client.force_authenticate(self.user1)
        data = {'rate':5, 'content':'123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       

    def test_post_comments_client_correct_data(self):
        url = reverse('comments-of-product', args=(self.product1.id,))
        self.client.force_authenticate(self.user2)
        data = {'rate':5, 'content':'123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_comments_client_incorrect_data(self):
        url = reverse('comments-of-product', args=(self.product1.id,))
        self.client.force_authenticate(self.user2)
        data = {'rate':5, 'content':'123', 'comment_of_reply':1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CommentDetailViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345')
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.comment1 = Comment.objects.create(user=self.user2, content='123', rate=5, product=self.product)
        self.comment2 = Comment.objects.create(user=self.user2, content='123', comment_of_reply=self.comment1, product=self.product)

    def test_get_own_comment(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_own_comment(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_not_own_comment(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user3)
        data = {'content':"321"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_own_comment_rate_with_correct_data(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user2)
        data = {'content':"321", "rate":2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_own_comment_rate_with_incorrect_data(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment2.id))
        self.client.force_authenticate(self.user2)
        data = {'content':"321", "rate":2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_own_comment_rate_with_comment_of_reply(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment2.id))
        self.client.force_authenticate(self.user2)
        data = {'content':"321", "rate":2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_comment(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_own_comment(self):
        url = reverse('comment-detail', args=(self.product.id, self.comment1.id))
        self.client.force_authenticate(self.user3)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CartViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345')
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)

    def test_get_cart_items(self):
        url = reverse('cart')
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_cart_item_client(self):
        url = reverse('cart')
        self.client.force_authenticate(self.user2)
        data = {'product':self.product.id, 'quantity':2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_cart_item_supplier(self):
        url = reverse('cart')
        self.client.force_authenticate(self.user1)
        data = {'product':self.product.id, 'quantity':2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CartDetailViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345')
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.cart_item = CartItem.objects.create(product=self.product, user=self.user2, quantity=5)

    def test_get_cart_item_detail_supplier(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_own_cart_item_detail_client(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user3)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_own_cart_item_detail_client(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_not_own_cart_item_detail(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user3)
        data = {'quantity':2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_own_cart_item_detail(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user3)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_own_cart_item_detail(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user2)
        data = {'quantity':2}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_own_cart_item_detail(self):
        url = reverse('cart-detail', args=(self.cart_item.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderListViewTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='mint', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
    
    def test_order_list_client(self):
        url = reverse('orders')
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_supplier(self):
        url = reverse('orders')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderCreateViewTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint1', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345', is_supplier=True)
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.cart_item1 = CartItem.objects.create(product=self.product, user=self.user1, quantity=5)
        self.cart_item2 = CartItem.objects.create(product=self.product, user=self.user1, quantity=5)
        self.cart_item3 = CartItem.objects.create(product=self.product, user=self.user1, quantity=5)
        self.cart_item4 = CartItem.objects.create(product=self.product, user=self.user1, quantity=5)
        self.cart_item5 = CartItem.objects.create(product=self.product, user=self.user2, quantity=5)

    def test_create_order(self):
        url = reverse('checkout-cart')
        self.client.force_authenticate(self.user1)
        data = {'ids':[self.cart_item1.id, self.cart_item2.id]}
        self.assertEqual(CartItem.objects.filter(user=self.user1).count(), 4)
        self.assertEqual(OrderItem.objects.all().count(), 0)
        response = self.client.post(url, data, format='json')
        self.assertEqual(CartItem.objects.filter(user=self.user1).count(), 2)
        self.assertEqual(OrderItem.objects.all().count(), 2)
        self.assertEqual(Order.objects.filter(user=self.user1).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_with_not_own_cart_item(self):
        url = reverse('checkout-cart')
        self.client.force_authenticate(self.user1)
        data = {'ids':[self.cart_item5.id,]}
        response = self.client.post(url, data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoriesViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint1', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345', is_staff=True)

    def test_get_categories_supplier(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories_client(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories_admin(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user3)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_categories_supplier(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user1)
        data = {"title":'qwf', "description":"123"}
        response = self.client.post(url, data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_categories_supplier(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user2)
        data = {"title":'qwf', "description":"123"}
        response = self.client.post(url, data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_categories_supplier(self):
        url = reverse('categories-list')
        self.client.force_authenticate(self.user3)
        data = {"title":'qwf', "description":"123"}
        response = self.client.post(url, data, format='json')   
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoryDetailViewTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint1', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345')
        self.user3 = User.objects.create(username='mint3', password='12345', is_staff=True)

    def test_get_category_detail_supplier(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_detail_client(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_detail_admin(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user3)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_category_detail_supplier(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user1)
        data = {"title":'qwf', "description":"123"}
        response = self.client.patch(url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_detail_client(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user2)
        data = {"title":'qwf', "description":"123"}
        response = self.client.patch(url, data, format='json')    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_category_detail_admin(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user3)
        data = {"title":'qwf', "description":"123"}
        response = self.client.patch(url, data, format='json')      
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_detail_supplier(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_detail_client(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_detail_admin(self):
        url = reverse('category-detail', args=(self.category.id,))
        self.client.force_authenticate(self.user3)
        response = self.client.delete(url)   
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class ProductPictureView(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint1', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345', is_supplier=True)
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.picure1 = ProductPicture.objects.create(product=self.product, picture='123.jpg')

    def test_get_picture_owner(self):
        url = reverse('products-pictures', args=(self.product.id,))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_picture_not_owner(self):
        url = reverse('products-pictures', args=(self.product.id,))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductPictureDetailView(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(title='123', description='123')
        self.user1 = User.objects.create(username='mint1', password='12345', is_supplier=True)
        self.user2 = User.objects.create(username='mint2', password='12345', is_supplier=True)
        self.product = Product.objects.create(title='Iphone', description='Iphone_x', price=12345, category=self.category, user=self.user1)
        self.picure1 = ProductPicture.objects.create(product=self.product, picture='123.jpg')

    def test_get_picture_owner(self):
        url = reverse('products-pictures-detail', args=(self.product.id, self.picure1.id))
        self.client.force_authenticate(self.user1)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_picture_not_owner(self):
        url = reverse('products-pictures-detail', args=(self.product.id, self.picure1.id))
        self.client.force_authenticate(self.user2)
        response = self.client.get(url)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_picture_not_owner(self):
        url = reverse('products-pictures-detail', args=(self.product.id, self.picure1.id))
        self.client.force_authenticate(self.user2)
        response = self.client.delete(url)   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_picture_owner(self):
        url = reverse('products-pictures-detail', args=(self.product.id, self.picure1.id))
        self.client.force_authenticate(self.user1)
        response = self.client.delete(url)   
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)