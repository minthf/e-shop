from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='products-list'),
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='products-detail'),
    path('product_detail/<int:pk>/pictures', ProductPicturesListView.as_view(), name='products-pictures'),
    path('product_detail/<int:pk>/pictures/<int:alt_pk>', ProductPictureDetailView.as_view(), name='products-pictures-detail'),
    path('comments_of_product/<int:pk>/', CommentsView.as_view(), name='comments-of-product'),
    path('cart/', CartView.as_view(), name='cart')
]
