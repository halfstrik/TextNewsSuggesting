from time import sleep
from datetime import datetime

from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            print str(datetime.now()) + ' Run texts_tf_idf_fill_key_words...'
            management.call_command('texts_tf_idf_fill_key_words')
            print str(datetime.now()) + ' Finish texts_tf_idf_fill_key_words...'
            sleep(5)
