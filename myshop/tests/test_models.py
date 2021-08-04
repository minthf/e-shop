from django.test import TestCase
from myshop.models import (
    Product,
    Comment,
    CartItem,
    Category,
    OrderItem,
    Order,
    User,
    Promocode,
)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones", description="Phones"
        )

    def test_title_max_length(self):
        max_length = self.category._meta.get_field("title").max_length
        self.assertEquals(max_length, 50)

    def test_description_max_length(self):
        max_length = self.category._meta.get_field("description").max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_title(self):
        expected_category_name = self.category.title
        self.assertEquals(expected_category_name, str(self.category))


class ProductCommentTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones1", description="Phones"
        )
        self.user = User.objects.create(username="user", password="123456")
        self.product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=12345,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
        )

    def test_comment_name_is_id_user_product(self):
        comment = Comment.objects.create(
            product=self.product, content="123", rate=4, user=self.user
        )
        expected_comment_name = (
            f"{comment.id} {comment.user} {comment.product}"
        )
        self.assertEquals(expected_comment_name, str(comment))

    def test_comment_quantity_in_product(self):
        Comment.objects.create(
            product=self.product, content="123", rate=4, user=self.user
        )
        Comment.objects.create(
            product=self.product, content="123", rate=4, user=self.user
        )
        Comment.objects.create(
            product=self.product, content="123", rate=4, user=self.user
        )
        Comment.objects.create(
            product=self.product,
            content="123",
            user=self.user,
            comment_of_reply=Comment.objects.all().first(),
        )
        comment = Comment.objects.all().first()
        comment.rate = 5
        comment.save()
        self.assertEquals(self.product.quantity_rates, 3)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones1", description="Phones"
        )
        self.user = User.objects.create(username="user", password="123456")
        self.product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=12345,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
        )

    def test_product_name_is_title(self):
        expected_product_name = self.product.title
        self.assertEquals(expected_product_name, str(self.product))

    def test_product_rating_with_no_rate(self):
        expected_product_rating = 0
        self.assertEquals(expected_product_rating, self.product.rating)

    def test_product_rating_with_one_rate(self):
        Comment.objects.create(
            product=self.product,
            rate=5,
            content="5",
            user=User.objects.get(id=self.user.id),
        )
        expected_product_rating = 5
        self.assertEquals(expected_product_rating, self.product.rating)

    def test_product_rating_with_two_rate(self):
        Comment.objects.create(
            product=self.product,
            rate=5,
            content="5",
            user=User.objects.get(id=self.user.id),
        )
        Comment.objects.create(
            product=self.product,
            rate=3,
            content="3",
            user=User.objects.get(id=self.user.id),
        )
        expected_product_rating = 4
        self.assertEquals(expected_product_rating, self.product.rating)

    def test_product_rating_with_changed_rate(self):
        Comment.objects.create(
            product=self.product,
            rate=5,
            content="5",
            user=User.objects.get(id=self.user.id),
        )
        Comment.objects.create(
            product=self.product,
            rate=3,
            content="3",
            user=User.objects.get(id=self.user.id),
        )
        comment = Comment.objects.all().first()
        comment.rate = 3
        comment.save()
        self.product = Product.objects.get(id=self.product.id)
        expected_product_rating = 3
        self.assertEquals(expected_product_rating, self.product.rating)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones1", description="Phones"
        )
        self.user = User.objects.create(username="user", password="123456")
        self.product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=12345,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
        )

    def test_cart_item_name_is_id_user_product_quantity(self):
        cart_item = CartItem.objects.create(
            product=self.product, user=self.user, quantity=5
        )
        expected_cart_item_name = f"{cart_item.id} {cart_item.user} {cart_item.product} - {cart_item.quantity}"
        self.assertEquals(expected_cart_item_name, str(cart_item))

    def test_cart_item_price(self):
        cart_item = CartItem.objects.create(
            product=self.product, user=self.user, quantity=5
        )
        expected_cart_item_price = 12345
        self.assertEquals(expected_cart_item_price, cart_item.price)

    def test_cart_item_price_with_discount(self):
        product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=1000,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
            discount=50,
        )
        cart_item = CartItem.objects.create(
            product=product, user=self.user, quantity=5
        )
        expected_cart_item_price = 500
        self.assertEquals(expected_cart_item_price, cart_item.price)


class OrerItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones1", description="Phones"
        )
        self.user = User.objects.create(username="user", password="123456")
        self.product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=12345,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
        )
        self.order = Order.objects.create(user=self.user, price=1, price_with_discount=1)

    def test_order_item_name_is_id_user_product_quantity(self):
        order_item = OrderItem.objects.create(
            product=self.product, quantity=6, price=1, order=self.order
        )
        expected_order_item_name = (
            f"{order_item.id} {order_item.product} - {order_item.quantity}"
        )
        self.assertEquals(expected_order_item_name, str(order_item))


class OrerModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="phones1", description="Phones"
        )
        self.user = User.objects.create(username="user", password="123456")
        self.product = Product.objects.create(
            title="Iphone",
            description="Iphone_x",
            price=12345,
            category=Category.objects.get(id=self.category.id),
            user=User.objects.get(id=self.user.id),
        )

    def test_order_name_is_id_user_product_quantity(self):
        order = Order.objects.create(user=self.user, price=1, price_with_discount=1)
        expected_order_name = f"{order.id} {order.user} {order.status} {order.price} - {order.price_with_discount}"
        self.assertEquals(expected_order_name, str(order))


class PromocodeModelTest(TestCase):
    def setUp(self):
        self.promocode = Promocode.objects.create(code="twenty", discount=20)

    def test_promocode_name_is_code_discount(self):
        expected_promocode_name = (
            f"{self.promocode.code} - {self.promocode.discount}"
        )
        self.assertEquals(expected_promocode_name, str(self.promocode))
