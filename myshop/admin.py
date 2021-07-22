from django.contrib import admin
from .models import (
    Product,
    Category,
    CartItem,
    Comment,
    ProductPicture,
    OrderItem,
    Order,
    User,
    Promocode,
)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Comment)
admin.site.register(ProductPicture)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Promocode)