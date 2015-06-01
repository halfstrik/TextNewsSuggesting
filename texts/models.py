from django.db import models
from tagging.models import Tag


class Source(models.Model):
    name = models.CharField(max_length=255)
    feed_link = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Text(models.Model):
    source = models.ForeignKey(Source)
    title = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)

    days_to_life = models.IntegerField(default=1)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    # tags = TagField()

    def __unicode__(self):
        return self.title


class TagRelationship(models.Model):
    first_tag = models.ForeignKey(Tag, related_name='tag_first')
    second_tag = models.ForeignKey(Tag, related_name='tag_second')
    weigh = models.PositiveSmallIntegerField()
