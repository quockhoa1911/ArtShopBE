from django.db import models
import uuid


# Create your models here.
class BaseModel(models.Model):
    objects = models.manager
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('create_at',)
