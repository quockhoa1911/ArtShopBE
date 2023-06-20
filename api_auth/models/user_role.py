from django.db import models
from api_base.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.


class Role(BaseModel):
    name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = "roles"


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True, default="No Name")
    password = models.CharField(max_length=256, null=True, blank=True)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, default=None, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    visa_card = models.CharField(max_length=16, null=True, blank=True, default=None)
    is_completed = models.BooleanField(default=False)
    address = models.CharField(max_length=256, null=True, blank=True, default=None)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
