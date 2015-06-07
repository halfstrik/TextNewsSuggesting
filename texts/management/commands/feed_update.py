from time import mktime
from datetime import datetime

from django.core.management import BaseCommand
import feedparser
import pytz

from sklearn.feature_extraction.text import strip_tags

from TextNewsSuggesting import settings
from texts.models import Source, Text, SourceTag, SourceTaggedItem


def limit_string_length(s, l):
    return s if len(s) <= l else s[:l]


class Command(BaseCommand):
    def handle(self, *args, **options):
        sources = Source.objects.all()
        for source in sources:
            d = feedparser.parse(source.feed_link)
            for entry in d.entries:
                try:
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
                    tags_list = []
                    if 'tags' in entry:
                        for tag in entry.tags:
                            tag_name = source.name + ': ' + tag.term
                            tag_name = tag_name.replace('"', '')
                            tag_name = limit_string_length(tag_name, settings.MAX_TAG_LENGTH)
                            tags_list.append(tag_name)
                    text, new = Text.objects.get_or_create(source=source,
                                                           title=title,
                                                           published=published,
                                                           link=link)
                    if new:
                        text.description = description
                        text.save()
                        for tag_name in tags_list:
                            source_tag, new = SourceTag.objects.get_or_create(name=tag_name,
                                                                              slug=tag_name,
                                                                              source=source)
                            SourceTaggedItem.objects.create(content_object=text, tag=source_tag)

                except Text.MultipleObjectsReturned:
                    pass
                except:
                    print 'Some error, skip entry of ' + str(source)
