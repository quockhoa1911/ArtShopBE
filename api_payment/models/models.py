from django.db import models
from api_base.models import BaseModel
from api_auth.models import User
from api_product.models import Products


# Create your models here.


class Payments(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='payment', default=None, null=True,
                             blank=True)
    payed = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'payments'


class PaymentDetails(BaseModel):
    payment = models.ForeignKey(to=Payments, on_delete=models.CASCADE, related_name='paymentdetail', default=None,
                                null=True, blank=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name='paymentdetail', default=None,
                                null=True, blank=True)

    class Meta:
        db_table = 'payment_details'
