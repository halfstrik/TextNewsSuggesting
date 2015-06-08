from datetime import datetime, timedelta
from optparse import make_option

from django.contrib.contenttypes.models import ContentType

from django.core.management import BaseCommand
import pytz

from texts.models import Text, KeyNormalizedWords, CommonTaggedItem
from texts.signals import normalize_words


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False),
    )

    def handle(self, *args, **options):
        not_moderated_texts = Text.objects.filter(is_moderated=False)
        if not options.get('all'):
            not_moderated_texts = not_moderated_texts.filter(
                created__gt=pytz.timezone('Europe/Moscow').localize(datetime.now() - timedelta(minutes=4)))
        all_key_words = KeyNormalizedWords.objects.all()
        for text in not_moderated_texts:
            all_words = unicode(text.title) + ' ' + unicode(text.description) + ' ' + unicode(text.body)
            all_words_normalized = normalize_words(all_words)

            for key_words in all_key_words:
                if key_words.words in all_words_normalized:
                    tag = key_words.tag
                    CommonTaggedItem.objects.get_or_create(tag=tag,
                                                           object_id=text.id,
                                                           content_type=ContentType.objects.get_for_model(Text))
