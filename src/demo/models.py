from django.db import models


# Create your models here.

class PaperConfig(models.Model):
    owner = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    config = models.TextField(max_length=21844)
