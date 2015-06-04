from time import mktime
from datetime import datetime

from django.core.management import BaseCommand
import feedparser
import pytz
from sklearn.feature_extraction.text import strip_tags
from tagging.models import Tag

from TextNewsSuggesting import settings

from texts.models import Source, Text


def limit_string_length(s, l):
    return s if len(s) <= l else s[:l]


class Command(BaseCommand):
    def handle(self, *args, **options):
        sources = Source.objects.all()
        for source in sources:
            d = feedparser.parse(source.feed_link)
            for entry in d.entries:
                description = entry.get('description', None)
                if description:
                    description = strip_tags(description)
                title = entry.get('title', description)
                if not title:
                    continue
                link = entry.get('link', None)
                if 'published_parsed' in entry:
                    published = datetime.fromtimestamp(mktime(entry.published_parsed)).replace(tzinfo=pytz.utc)
                else:
                    published = None
                if 'tags' in entry:
                    tags_list = []
                    for tag in entry.tags:
                        tag_name = source.name + ': ' + tag.term
                        tag_name = tag_name.replace('"', '')
                        tag_name = limit_string_length(tag_name, settings.MAX_TAG_LENGTH)
                        tags_list.append('"' + tag_name + '"')
                    publisher_tags = ', '.join(tags_list)
                else:
                    publisher_tags = None
                try:
                    text, new = Text.objects.get_or_create(source=source,
                                                           title=title,
                                                           published=published,
                                                           link=link)
                    if new:
                        text.description = description
                        text.save()
                        Tag.objects.update_tags(text, publisher_tags)
                except Text.MultipleObjectsReturned:
                    pass
