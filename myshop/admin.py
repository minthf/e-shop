from django.contrib import admin
from .models import Product, Category, CartItem, Comment, ProductPicture

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Comment)
admin.site.register(ProductPicture)

