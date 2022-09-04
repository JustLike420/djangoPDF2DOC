from django.db import models
from django.conf import settings


# Create your models here.

class UsersFiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField()
    ordered_date = models.DateTimeField(auto_now_add=True)
