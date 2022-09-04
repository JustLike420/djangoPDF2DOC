from django.db import models
from django.conf import settings


# Create your models here.

class UsersFiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_date) + ' | ' + self.file.name
