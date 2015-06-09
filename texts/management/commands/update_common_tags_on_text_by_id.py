from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, CommandError

from texts.models import Text, KeyNormalizedWords, CommonTaggedItem
from texts.signals import normalize_words


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('text_id', nargs='+', type=int)

    def handle(self, *args, **options):
        if 'text_id' not in options.keys():
            raise CommandError('Need text id')
        text_id = options['text_id'][0]
        text = Text.objects.get(id=text_id)
        if text.is_moderated:
            raise CommandError('Text already moderated')
        all_key_words = KeyNormalizedWords.objects.all()
        all_words = unicode(text.title) + ' ' + unicode(text.description) + ' ' + unicode(text.body)
        all_words_normalized = normalize_words(all_words)

        for key_words in all_key_words:
            if key_words.words in all_words_normalized:
                tag = key_words.tag
                CommonTaggedItem.objects.get_or_create(tag=tag,
                                                       object_id=text.id,
                                                       content_type=ContentType.objects.get_for_model(Text))
