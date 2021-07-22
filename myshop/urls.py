from django.urls import path
from .views import (
    CategoriesView,
    CategoryDetailView,
    ProductsListView,
    ProductDetailView,
    ProductPicturesListView,
    ProductPictureDetailView,
    CommentsView,
    CommentDetailView,
    CartView,
    CartDetailView,
    OrderCreateView,
    OrderListView,
    PromocodeListView,
    PromocodeDetailView,
)


urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories-list"),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path("products/", ProductsListView.as_view(), name="products-list"),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path(
        "products/<int:pk>/pictures/",
        ProductPicturesListView.as_view(),
        name="products-pictures",
    ),
    path(
        "products/<int:pk>/pictures/<int:alt_pk>/",
        ProductPictureDetailView.as_view(),
        name="products-pictures-detail",
    ),
    path(
        "products/<int:pk>/comments/",
        CommentsView.as_view(),
        name="comments-of-product",
    ),
    path(
        "products/<int:pk>/comments/<int:alt_pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    path("cart/checkout/", OrderCreateView.as_view(), name="checkout-cart"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("promocodes/", PromocodeListView.as_view(), name="promocodes-list"),
    path(
        "promocodes/<int:pk>/",
        PromocodeDetailView.as_view(),
        name="promocode-detail",
    ),
]
