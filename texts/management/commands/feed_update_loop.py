from time import sleep

from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        management.call_command('update_common_tags_on_non_moderated_texts', all=True)
        while True:
            print 'Run feed_update...'
            management.call_command('feed_update')
            print 'Creating common tags...'
            management.call_command('update_common_tags_on_non_moderated_texts')
            print 'Finish feed_update, waiting for the next run...'
            sleep(120)
