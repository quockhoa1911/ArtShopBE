from django.db import models
from api_base.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "category"
