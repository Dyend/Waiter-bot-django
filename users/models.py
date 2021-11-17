
from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class ExtendedUser(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='logged_in_user') 
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.user.username

    @property
    def username(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'extended_users'
