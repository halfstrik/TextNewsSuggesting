from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Text(models.Model):
    source = models.ForeignKey(Source)
    date = models.DateTimeField()
    days_to_life = models.IntegerField(default=1)
    title = models.CharField(max_length=1024, unique=True)
    body = models.TextField()
    keywords = models.CharField(max_length=255)
