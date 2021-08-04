from django.test import TestCase
from myshop.models import (
    Product,
    Category,
    CartItem,
    Comment,
    ProductPicture,
    User,
)
from myshop.serializers import (
    CommentSerializer,
    CategorySerializer,
    CartSerializer,
    PictureSerializer,
)
from decouple import config
from collections import OrderedDict


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="123", description="123")

    def test_category_serializer_data(self):
        serializer = CategorySerializer(self.category)
        expected_data = {
            "id": self.category.id,
            "title": f"{self.category.title}",
            "description": f"{self.category.description}",
        }
        self.assertEquals(expected_data, serializer.data)


class CommentSerializerTest(TestCase):
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
        self.comment1 = Comment.objects.create(
            product=self.product, content="1", rate=1, user=self.user
        )
        self.comment2 = Comment.objects.create(
            product=self.product,
            content="2",
            comment_of_reply=self.comment1,
            user=self.user,
        )
        self.comment3 = Comment.objects.create(
            product=self.product,
            content="3",
            comment_of_reply=self.comment2,
            user=self.user,
        )

    def test_comment_serializer_data(self):
        serializer = CommentSerializer(Comment.objects.all().first())
        expected_data = {
            "id": self.comment1.id,
            "rate": self.comment1.rate,
            "content": f"{self.comment1.content}",
            "creation_date": f"{self.comment1.creation_date}",
            "product": self.comment1.product.id,
            "user": self.comment1.user.id,
            "replies": [
                OrderedDict(
                    [
                        ("id", self.comment2.id),
                        ("rate", None),
                        ("content", f"{self.comment2.content}"),
                        ("creation_date", f"{self.comment2.creation_date}"),
                        ("product", self.comment2.product.id),
                        ("user", self.comment1.user.id),
                        (
                            "replies",
                            [
                                OrderedDict(
                                    [
                                        ("id", self.comment3.id),
                                        ("rate", None),
                                        (
                                            "content",
                                            f"{self.comment3.content}",
                                        ),
                                        (
                                            "creation_date",
                                            f"{self.comment3.creation_date}",
                                        ),
                                        ("product", self.comment3.product.id),
                                        ("user", self.comment1.user.id),
                                        ("replies", []),
                                    ]
                                )
                            ],
                        ),
                    ]
                )
            ],
        }
        self.assertEquals(expected_data, serializer.data)


class PictureSerializerTest(TestCase):
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
        self.picture = ProductPicture.objects.create(
            product=self.product, picture="123"
        )

    def test_picture_url(self):
        serializer = PictureSerializer(self.picture)
        expected_data = {
            "id": self.picture.id,
            "picture": config("DOMEN") + "/media/" + str(self.picture.picture),
            "product": self.product.id,
        }
        self.assertEquals(expected_data, serializer.data)
