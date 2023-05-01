from django.db import models
from api_base.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.


class Role(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "roles"


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, default=None, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
