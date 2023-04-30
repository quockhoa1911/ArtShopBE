from django.db import models
from api_base.models import BaseModel
from api_auth.models import Author


# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "category"


class Products(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    categories = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="product", default=None,
                                   null=True, blank=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="product", default=None, null=True,
                               blank=True)
    sold = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = "products"
