from django.db import models
from api_base.models import BaseModel
from api_auth.models import Author, User
from api_product.models import Category


# Create your models here.

class Products(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, default=None)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="product", default=None,
                                 null=True, blank=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="product", default=None, null=True,
                               blank=True)
    sold = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    price = models.FloatField(max_length=256, null=True, blank=True)
    start_auction = models.CharField(max_length=256, null=True, blank=True, default=None)
    end_auction = models.CharField(max_length=256, null=True, blank=True, default=None)
    auction_price = models.FloatField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "products"


class ImageProduct(BaseModel):
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name="imageproduct", default=None,
                                null=True, blank=True)
    image = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "image_products"


class AuctionProduct(BaseModel):
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name="auctionproduct", default=None,
                                null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="auctionproduct", default=None, null=True,
                             blank=True)
    is_success = models.BooleanField(default=False, null=True, blank=True)
    auction_price = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = "auction_products"
