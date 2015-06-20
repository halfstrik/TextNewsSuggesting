from time import sleep
from datetime import datetime

from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            print str(datetime.now()) + ' Run feed_update...'
            management.call_command('feed_update')
            print str(datetime.now()) + ' Finish feed_update...'
            sleep(120)
