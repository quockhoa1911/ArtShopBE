from django.db import models
from api_base.models import BaseModel
from api_auth.models import Role


class Author(BaseModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    origin = models.CharField(max_length=256, blank=True, null=True)
    birthday = models.CharField(max_length=256, blank=True, null=True)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, related_name="author", default=None, null=True,
                             blank=True)

    class Meta:
        db_table = "authors"
