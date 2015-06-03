from django.contrib.auth.models import User
from django.db import models
from tagging.models import Tag


class Source(models.Model):
    name = models.CharField(max_length=255)
    feed_link = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class PropertyFirst(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class PropertySecond(models.Model):
    name = models.CharField(max_length=255)

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

    property_first = models.ForeignKey(PropertyFirst, blank=True, null=True)
    property_second = models.ForeignKey(PropertySecond, blank=True, null=True)

    is_moderated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def comments_count(self):
        return Comment.objects.filter(news=self.id).count()


class TagRelationship(models.Model):
    first_tag = models.ForeignKey(Tag, related_name='tag_first')
    second_tag = models.ForeignKey(Tag, related_name='tag_second')

    class Meta:
        unique_together = ('first_tag', 'second_tag')

    RANKS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),)

    weigh = models.PositiveSmallIntegerField(choices=RANKS)


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, editable=False)
    news = models.ForeignKey(Text, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
