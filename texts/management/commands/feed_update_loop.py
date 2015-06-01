from time import sleep

from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            print 'Run feed_update...'
            management.call_command('feed_update')
            print 'Finish feed_update, waiting for the next run...'
            sleep(120)