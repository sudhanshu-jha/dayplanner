from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Goal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.title
