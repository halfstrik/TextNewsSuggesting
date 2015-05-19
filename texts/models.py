from django.db import models


class Text(models.Model):
    title = models.CharField(max_length=1024, unique=True)
    body = models.TextField()
