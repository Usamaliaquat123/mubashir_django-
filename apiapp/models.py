from django.db import models
from accountapp.models import User
import uuid

# Header API Keys Model.
class APIAuthKey(models.Model):
    key             = models.UUIDField(primary_key=True, default= uuid.uuid4)
    isRevoked       = models.BooleanField(default=False)
    ipaddress       = models.GenericIPAddressField(null=True, blank=True)
    browserinfo     = models.TextField(null=True, blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True, null=True)
    createdBy       = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name        = "API Auth Key"
        verbose_name_plural = "API Auth Keys"