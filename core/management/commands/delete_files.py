
from django.core.management.base import BaseCommand
from ...models import File

def DeleteFiles():
    deleted = 0
    for file in File.objects.all():
        file.delete()
        deleted += 1
    print('DELETED', deleted, 'File objects')

class Command(BaseCommand):

    def handle(self, *args, **options):
        DeleteFiles()
