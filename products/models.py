from django.db import models
# from avina.storage import select_storage
from avina.settings import AUTH_USER_MODEL
from django.db.models.deletion import CASCADE, RESTRICT
from django.contrib.auth import get_user_model


class CartItemStatus:
    PENDING = "Pending"
    SOLD = "Sold"
    CANCELLED = "Cancelled"

    @staticmethod
    def choices():
        return (
            (CartItemStatus.PENDING, CartItemStatus.PENDING),
            (CartItemStatus.SOLD, CartItemStatus.SOLD),
            (CartItemStatus.CANCELLED, CartItemStatus.CANCELLED),
        )

class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0   )    
    category = models.ForeignKey(
        "categories.Category", on_delete=RESTRICT, related_name="products")
    photo1 = models.ImageField(upload_to="products",blank=True,null=True,default=None)
    photo2 = models.ImageField(upload_to="products",blank=True,null=True,default=None)
    photo3 = models.ImageField(upload_to="products",blank=True,null=True,default=None)
    photo4 = models.ImageField(upload_to="products",blank=True,null=True,default=None)
    description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=RESTRICT, related_name="products")
    sold = models.BooleanField(default=False)

    def __repr__(self):
        return "Product:\t{}\nDescription:\t{}".format(self.name, self.description)

class CartItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(choices=CartItemStatus.choices(), max_length=20, default=CartItemStatus.PENDING)
    seller_confirmation = models.CharField(choices=CartItemStatus.choices(), max_length=20, default=CartItemStatus.PENDING)
    buyer_confirmation = models.CharField(choices=CartItemStatus.choices(), max_length=20, default=CartItemStatus.PENDING)

    def make_sold(self):
        self.status = CartItemStatus.SOLD

    def cancel(self):
        self.status = CartItemStatus.CANCELLED

    @property
    def seller(self):
        return self.product.added_by
