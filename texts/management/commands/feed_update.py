from time import mktime
from datetime import datetime

from django.core.management import BaseCommand
import feedparser
from sklearn.feature_extraction.text import strip_tags

from texts.models import Source, Text


class Command(BaseCommand):
    def handle(self, *args, **options):
        sources = Source.objects.all()
        for source in sources:
            d = feedparser.parse(source.feed_link)
            for entry in d.entries:
                title = entry.get('title', None)
                description = entry.get('description', None)
                if description:
                    description = strip_tags(description)
                link = entry.get('link', None)
                if 'published_parsed' in entry:
                    published = datetime.fromtimestamp(mktime(entry.published_parsed))
                else:
                    published = None
                if 'tags' in entry:
                    tags_list = []
                    for tag in entry.tags:
                        tags_list.append(tag.term)
                    publisher_tags = ', '.join(tags_list)
                else:
                    publisher_tags = None
                Text.objects.get_or_create(source=source,
                                           title=title,
                                           description=description,
                                           link=link,
                                           published=published,
                                           publisher_tags=publisher_tags)
