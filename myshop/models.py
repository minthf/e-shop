from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

class Category(models.Model):
    '''Category of Products in shop'''
    title = models.CharField(verbose_name='Title', max_length=50, unique=True)
    description = models.CharField(verbose_name='Description', max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    '''Product in shop'''
    title = models.CharField(verbose_name='Title', max_length=50)
    description = models.CharField(verbose_name='Description', max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    supplier = models.ForeignKey(User, related_name='supplier', on_delete=models.CASCADE)
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_rates = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

class ProductPicture(models.Model):
    '''Pictures of product'''
    product = models.ForeignKey(Product, related_name='pictures', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images/products/%Y/%m/%d', blank=True)


class Comment(models.Model):
    '''Comment about Product'''
    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    product = models.ForeignKey(Product, related_name='comment', on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='comment_author', on_delete=models.CASCADE)
    rate = models.IntegerField(choices=rates, blank=True, null=True)
    content = models.CharField(verbose_name='Content', max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    comment_of_reply = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.client} {self.product}"


@receiver(signals.pre_save, sender=Comment)
def update_product_rate(sender, instance, **kwargs):
    """ Update product rating when added or changed rate in comments"""
    if instance.id:
        old_comment = Comment.objects.get(pk=instance.id)
        instance.product.rating = ((instance.product.rating*instance.product.quantity_rates)+instance.rate-old_comment.rate)/instance.product.quantity_rates
    else:
        instance.product.quantity_rates += 1
        instance.product.rating = ((instance.product.rating*(instance.product.quantity_rates-1))+instance.rate)/instance.product.quantity_rates
    instance.product.save()


class CartItem(models.Model):
    """Cart item in clients carts"""
    status = models.BooleanField()
    client = models.ForeignKey(User, related_name='cart_owner', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.client} {self.product} - {self.quantity}"
