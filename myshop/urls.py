from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='products-detail'),
    path('comments_of_product/<int:pk>/', CommentsView.as_view(), name='comments-of-product'),
]
