from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from taggit.models import TagBase, ItemBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode


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
    body = models.TextField(blank=True, null=True)
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

    def original_link(self):
        return '<a href="%s">click me with MIDDLE mouse</a>' % self.link

    original_link.allow_tags = True

    def auto_assign_tags_link(self):
        return '<a href="%s">click me with LEFT mouse</a>' % reverse('assign_common_tags_to_text', args=[self.id])

    auto_assign_tags_link.allow_tags = True


class SourceTag(TagBase):
    source = models.ForeignKey(Source)

    class Meta:
        verbose_name = _("Source tag")
        verbose_name_plural = _("Source tags")


class SourceTaggedItemBase(ItemBase):
    tag = models.ForeignKey(SourceTag, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True


class SourceTaggedItem(GenericTaggedItemBase, SourceTaggedItemBase):
    class Meta:
        verbose_name = _("Source Tagged Item")
        verbose_name_plural = _("Source Tagged Items")


class CommonTag(TagBase):
    associations = models.CharField(max_length=1024)

    def save(self):
        if not self.pk:
            self.slug = slugify(unidecode(self.name))
        super(CommonTag, self).save()

    class Meta:
        verbose_name = _("Common tag")
        verbose_name_plural = _("Common tags")


WEAK = 'WK'
AVERAGE = 'AV'
STRONG = 'ST'
STRENGTH = ((WEAK, 'Weak'), (AVERAGE, 'Average'), (STRONG, 'Strong'))


class CommonTagRelationship(models.Model):
    first_tag = models.ForeignKey(CommonTag, related_name='first_tag')
    second_tag = models.ForeignKey(CommonTag, related_name='second_tag')

    weigh = models.CharField(max_length=2, choices=STRENGTH, default=AVERAGE)

    class Meta:
        unique_together = ('first_tag', 'second_tag')


class CommonTaggedItemBase(ItemBase):
    tag = models.ForeignKey(CommonTag, related_name="%(app_label)s_%(class)s_items")

    class Meta:
        abstract = True


class CommonTaggedItem(GenericTaggedItemBase, CommonTaggedItemBase):
    weigh = models.CharField(max_length=2, choices=STRENGTH, default=AVERAGE)

    class Meta:
        verbose_name = _("Common Tagged Item")
        verbose_name_plural = _("Common Tagged Items")


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, editable=False)
    news = models.ForeignKey(Text, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text


class KeyNormalizedWords(models.Model):
    words = models.CharField(max_length=255)
    tag = models.ForeignKey(CommonTag)

    class Meta:
        unique_together = ('words', 'tag')
        verbose_name_plural = _("Key normalized words")

    def __unicode__(self):
        return self.words
